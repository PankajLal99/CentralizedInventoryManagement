import uuid
from django.db import models
from django.core.exceptions import ValidationError
from management.utils.inventory_logic import *

# Vendor Model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    gst = models.CharField(max_length=15)
    details = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Sub-Category Model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Unit Model
class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    reorder_level = models.PositiveIntegerField()
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.barcode:  # Generate a barcode only if it's not already set
            self.barcode = self.generate_unique_barcode()
        super().save(*args, **kwargs)

    def generate_unique_barcode(self):
        # Generate a unique barcode and ensure it's not already in the database
        while True:
            barcode = f"PROD-{uuid.uuid4().hex[:12].upper()}"  # Generate a 12-character barcode
            if not Product.objects.filter(barcode=barcode).exists():
                return barcode

    def __str__(self):
        return self.name


# Warehouse Model
class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Purchase Model
class Purchase(models.Model):
    purchase_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    vendor_invoice_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Purchase {self.id} - {self.vendor.name}"


# Purchase Products Model
class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.price} - {self.purchase.purchase_date}"
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the record is being updated
            original = PurchaseProduct.objects.get(pk=self.pk)
            handle_purchase_edit(original, self.quantity)
        else:
            update_inventory(
                        product=self.product,
                        warehouse=self.purchase.warehouse,
                        quantity_delta=self.quantity
                    )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        handle_purchase_deletion(self)
        super().delete(*args, **kwargs)

# Purchase Return Model
class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    return_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Return {self.id} - {self.product.name}"


# Purchase Products Sale Model
class PurchaseProductSale(models.Model):
    purchase_product = models.ForeignKey(PurchaseProduct, on_delete=models.CASCADE)
    margin_percent = models.DecimalField(max_digits=5, decimal_places=2)
    total_margin = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_gst = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Sale {self.purchase_product.product.name}"


# Customer Details Model
class CustomerDetails(models.Model):
    name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.CharField(max_length=15)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Sale Model
class Sale(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    gst = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id}"


# Sale Products Model
class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    purchase_product_sale = models.ForeignKey(PurchaseProductSale, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.sale.id} - {self.purchase_product_sale.purchase_product.product.name}"

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the record is being updated
            original = SaleProduct.objects.get(pk=self.pk)
            handle_sale_edit(original, self.quantity)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        handle_sale(self, is_deletion=True)
        super().delete(*args, **kwargs)

# Sale Return Model
class SaleReturn(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    return_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Return {self.id} - {self.product.name}"


# Inventory Model
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_available = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"


# Stock Transfer Model
class StockTransfer(models.Model):
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='source_warehouse')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='destination_warehouse')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transfer {self.product.name} - {self.source_warehouse.name} to {self.destination_warehouse.name}"
    
    def save(self, *args, **kwargs):
        # Ensure valid stock transfer before saving
        if self.source_warehouse == self.destination_warehouse:
            raise ValidationError("Source and destination warehouses cannot be the same.")
        if self.quantity <= 0:
            raise ValidationError("Transfer quantity must be greater than zero.")
        
        if self.pk:  # Check if the record is being updated
            original = StockTransfer.objects.get(pk=self.pk)
            handle_stock_transfer_edit(original, self.quantity)

        # Update inventory on save
        update_inventory_on_transfer(
            product=self.product,
            quantity=self.quantity,
            source_warehouse=self.source_warehouse,
            destination_warehouse=self.destination_warehouse
        )

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        handle_stock_transfer(self, is_deletion=True)
        super().delete(*args, **kwargs)