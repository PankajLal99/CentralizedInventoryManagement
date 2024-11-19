from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from management import models as md

# TODO : Whole Logic Test is pending and in to be done 

def update_inventory_on_purchase(product, quantity, warehouse):
    """Updates inventory when a purchase is made."""
    inventory, created = md.Inventory.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={'quantity_available': 0, 'reorder_level': 2}  # Default reorder level
    )
    inventory.quantity_available += quantity
    inventory.save()

def update_inventory_on_sale(product, quantity, warehouse):
    """Updates inventory when a sale is made."""
    inventory = md.Inventory.objects.get(product=product, warehouse=warehouse)
    if inventory.quantity_available < quantity:
        raise ValidationError("Insufficient stock for the sale.")
    inventory.quantity_available -= quantity
    inventory.save()

def update_inventory_on_transfer(product, quantity, source_warehouse, destination_warehouse):
    """Updates inventory for stock transfers."""
    source_inventory = md.Inventory.objects.get(product=product, warehouse=source_warehouse)
    if source_inventory.quantity_available < quantity:
        raise ValidationError("Insufficient stock in the source warehouse.")

    destination_inventory, created = md.Inventory.objects.get_or_create(
        product=product,
        warehouse=destination_warehouse,
        defaults={'quantity_available': 0, 'reorder_level': 2}  # Default reorder level
    )

    # Update inventory quantities atomically
    with transaction.atomic():
        source_inventory.quantity_available -= quantity
        source_inventory.save()

        destination_inventory.quantity_available += quantity
        destination_inventory.save()

def update_inventory(product, warehouse, quantity_delta):
    """Update inventory for a specific product in a warehouse."""
    inventory, created = md.Inventory.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={'quantity_available': 0, 'reorder_level': 2}
    )
    if inventory.quantity_available + quantity_delta < 0:
        raise ValidationError("Insufficient stock.")
    inventory.quantity_available += quantity_delta
    inventory.save()

def handle_purchase_deletion(purchase_product):
    """Adjust inventory when a purchase is deleted."""
    update_inventory(
        product=purchase_product.product,
        warehouse=purchase_product.purchase.warehouse,
        quantity_delta=-purchase_product.quantity
    )

def handle_sale(sale_product, is_deletion=False):
    """Adjust inventory on sale or sale deletion."""
    delta = -sale_product.quantity if not is_deletion else sale_product.quantity
    update_inventory(
        product=sale_product.purchase_product_sale.purchase_product.product,
        warehouse=sale_product.sale.warehouse,
        quantity_delta=delta
    )

def handle_stock_transfer(stock_transfer, is_deletion=False):
    """Adjust inventory for stock transfers."""
    delta = stock_transfer.quantity if is_deletion else -stock_transfer.quantity

    # Source Warehouse
    update_inventory(
        product=stock_transfer.product,
        warehouse=stock_transfer.source_warehouse,
        quantity_delta=delta
    )

    # Destination Warehouse
    update_inventory(
        product=stock_transfer.product,
        warehouse=stock_transfer.destination_warehouse,
        quantity_delta=-delta
    )

def handle_purchase_edit(purchase_product, new_quantity):
    """Handle inventory update when a purchase is edited."""
    original_quantity = purchase_product.quantity
    quantity_delta = new_quantity - original_quantity

    # Restore original quantity and apply the new change
    update_inventory(
        product=purchase_product.product,
        warehouse=purchase_product.purchase.warehouse,
        quantity_delta=quantity_delta
    )

def handle_sale_edit(sale_product, new_quantity):
    """Handle inventory update when a sale is edited."""
    original_quantity = sale_product.quantity
    quantity_delta = new_quantity - original_quantity

    # Restore original quantity and apply the new change
    update_inventory(
        product=sale_product.purchase_product_sale.purchase_product.product,
        warehouse=sale_product.sale.warehouse,
        quantity_delta=-quantity_delta
    )

def handle_purchase_return(purchase_product, return_quantity):
    """Handle inventory update for a purchase return."""
    if return_quantity > purchase_product.quantity:
        raise ValidationError("Return quantity exceeds purchased quantity.")

    update_inventory(
        product=purchase_product.product,
        warehouse=purchase_product.warehouse,
        quantity_delta=-return_quantity
    )

def handle_sale_return(sale_product, return_quantity):
    """Handle inventory update for a sale return."""
    if return_quantity > sale_product.quantity:
        raise ValidationError("Return quantity exceeds sold quantity.")

    update_inventory(
        product=sale_product.product,
        warehouse=sale_product.sale.warehouse,
        quantity_delta=return_quantity
    )

def handle_stock_transfer_edit(stock_transfer, new_quantity):
    """Handle inventory update when a stock transfer is edited."""
    original_quantity = stock_transfer.quantity
    quantity_delta = new_quantity - original_quantity

    if quantity_delta == 0:
        return  
    # Restore original transfer and apply the new change
    update_inventory(
        product=stock_transfer.product,
        warehouse=stock_transfer.source_warehouse,
        quantity_delta=-quantity_delta  # Subtract more if increasing, add back if decreasing
    )

    update_inventory(
        product=stock_transfer.product,
        warehouse=stock_transfer.destination_warehouse,
        quantity_delta=quantity_delta  # Add more if increasing, subtract if decreasing
    )