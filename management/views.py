from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import modelformset_factory
from .models import *
from .forms import *
from management.utils.inventory_logic import *

def home_page(request):
    return render(request, 'management/home.html',)

# List View to display all vendors
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})

# Create View to add a new vendor
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor-list')
    else:
        form = VendorForm()
    return render(request, 'vendor/vendor_form.html', {'form': form})

# Update View to edit an existing vendor
def vendor_update(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor-list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor/vendor_form.html', {'form': form})

# Delete View to delete an existing vendor
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor-list')
    return render(request, 'components/confirm_delete.html', {'object': vendor})

# List View to display all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

# Create View to add a new category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

# Update View to edit an existing category
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})

# Delete View to delete an existing category
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'components/confirm_delete.html', {'object': category})

# List View for SubCategories
def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'subcategory/subcategory_list.html', {'subcategories': subcategories})

# Create View for SubCategory
def subcategory_create(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory-list')
    else:
        form = SubCategoryForm()
    return render(request, 'subcategory/subcategory_form.html', {'form': form})

# Update View for SubCategory
def subcategory_update(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory-list')
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'subcategory/subcategory_form.html', {'form': form})

# Delete View for SubCategory
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory-list')
    return render(request, 'components/confirm_delete.html', {'object': subcategory})

# List View for Units
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'unit/unit_list.html', {'units': units})

# Create View for Unit
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit-list')
    else:
        form = UnitForm()
    return render(request, 'unit/unit_form.html', {'form': form})

# Update View for Unit
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit-list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'unit/unit_form.html', {'form': form})

# Delete View for Unit
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('unit-list')
    return render(request, 'components/confirm_delete.html', {'object': unit})

# List View for Products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

# Create View for Product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

# Update View for Product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

# Delete View for Product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    return render(request, 'components/confirm_delete.html', {'object': product})

# List View for Purchases
def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

# Create View for Purchase
def purchase_create(request):
    # Initialize the PurchaseForm
    purchase_form = PurchaseForm(request.POST or None)

    # Create the formset for PurchaseProduct
    PurchaseProductFormset = modelformset_factory(
        PurchaseProduct, form=PurchaseProductForm, extra=5, can_delete=True
    )
    # No instance, so we use an empty queryset
    formset = PurchaseProductFormset(request.POST or None, queryset=PurchaseProduct.objects.none())

    if request.method == 'POST':
        if purchase_form.is_valid() and formset.is_valid():
            # Save the Purchase instance
            purchase = purchase_form.save()
            # Save the PurchaseProduct instances linked to this purchase
            for form in formset:
                purchase_product = form.save(commit=False)
                if purchase_product:
                    purchase_product.purchase = purchase  # Associate with the newly created Purchase
                    purchase_product.save()
                    update_inventory(
                        product=purchase_product.product,
                        warehouse=purchase.warehouse,
                        quantity_delta=purchase_product.quantity
                    )

            return redirect('purchase-list')  # Redirect to purchase list after creation

    return render(request, 'purchase/purchase_form.html', {
        'purchase_form': purchase_form,
        'formset': formset,
    })

# Update View for Purchase
def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, id=pk)
    purchase_products = PurchaseProduct.objects.filter(purchase=purchase)

    purchase_form = PurchaseForm(request.POST or None, instance=purchase)
    PurchaseProductFormset = modelformset_factory(PurchaseProduct, form=PurchaseProductForm, can_delete=True,extra=5)
    formset = PurchaseProductFormset(request.POST or None, queryset=purchase_products)

    if request.method == 'POST':
        if purchase_form.is_valid() and formset.is_valid():
            purchase = purchase_form.save(commit=False)
            purchase.save()
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
                else:
                    purchase_product = form.save(commit=False)
                    if purchase_product:  # Only save non-empty instances
                        purchase_product.purchase = purchase
                        purchase_product.save()

            return redirect('purchase-list')

    return render(request, 'purchase/purchase_form.html', {
        'purchase_form': purchase_form,
        'formset': formset,
        'purchase': purchase,
    })

# Delete View for Purchase
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        purchase.delete()
        return redirect('purchase-list')
    return render(request, 'components/confirm_delete.html', {'object': purchase})


# Customer Views
def customer_create(request):
    if request.method == 'POST':
        form = CustomerDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list')  # Redirect to a customer list view
    else:
        form = CustomerDetailsForm()

    return render(request, 'customer/customer_form.html', {'form': form})


# Customer List View
def customer_list(request):
    customers = CustomerDetails.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})


def customer_update(request, pk):
    customer = get_object_or_404(CustomerDetails, id=pk)
    if request.method == 'POST':
        form = CustomerDetailsForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-list')
    else:
        form = CustomerDetailsForm(instance=customer)

    return render(request, 'customer/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(CustomerDetails, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer-list')
    return render(request, 'components/confirm_delete.html', {'object': customer})


# Warehouse Views
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse/warehouse_list.html', {'warehouses': warehouses})


def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse-list')
    else:
        form = WarehouseForm()

    return render(request, 'warehouse/warehouse_form.html', {'form': form})

def warehouse_update(request, pk):
    warehouse = get_object_or_404(Warehouse, id=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse-list')
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, 'warehouse/warehouse_form.html', {'form': form})


def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, id=pk)
    if request.method == 'POST':
        warehouse.is_active = False  # Soft delete
        warehouse.save()
        return redirect('warehouse-list')

    return render(request, 'components/confirm_delete.html', {'object': warehouse})

# Purchase Product Sale List
def purchase_product_sale_list(request):
    sales = PurchaseProductSale.objects.all()
    return render(request, 'purchase_product_sale/purchase_product_sale_list.html', {'sales': sales})


# Purchase Product Sale Create
def purchase_product_sale_create(request):
    if request.method == 'POST':
        form = PurchaseProductSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase-product-sale-list')
    else:
        form = PurchaseProductSaleForm()
    return render(request, 'purchase_product_sale/purchase_product_sale_form.html', {'form': form})


# Purchase Product Sale Update
def purchase_product_sale_update(request, pk):
    sale = get_object_or_404(PurchaseProductSale, pk=pk)
    if request.method == 'POST':
        form = PurchaseProductSaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('purchase-product-sale-list')
    else:
        form = PurchaseProductSaleForm(instance=sale)
    return render(request, 'purchase_product_sale/purchase_product_sale_form.html', {'form': form})


# Purchase Product Sale Delete
def purchase_product_sale_delete(request, pk):
    sale = get_object_or_404(PurchaseProductSale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('purchase-product-sale-list')
    return render(request, 'components/confirm_delete.html', {'object': sale})


# Sale List
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sale/sale_list.html', {'sales': sales})


# Sale Create with Sale Products
def sale_create(request):
    SaleProductFormset = modelformset_factory(SaleProduct, form=SaleProductForm, extra=1, can_delete=True)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        formset = SaleProductFormset(request.POST)
        if sale_form.is_valid() and formset.is_valid():
            sale = sale_form.save(commit=False)
            sale.subtotal = 0
            sale.total = 0
            sale.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    sale_product = form.save(commit=False)
                    sale_product.sale = sale
                    sale_product.save()
                    sale.subtotal += sale_product.total

            sale.total = sale.subtotal + (sale.subtotal * sale.gst / 100)
            sale.save()
            return redirect('sale-list')
    else:
        sale_form = SaleForm()
        formset = SaleProductFormset(queryset=SaleProduct.objects.none())

    return render(request, 'sale/sale_form.html', {'sale_form': sale_form, 'formset': formset})


# Sale Update
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    SaleProductFormset = modelformset_factory(SaleProduct, form=SaleProductForm, extra=1, can_delete=True)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST, instance=sale)
        formset = SaleProductFormset(request.POST, queryset=sale.saleproduct_set.all())
        if sale_form.is_valid() and formset.is_valid():
            sale = sale_form.save(commit=False)
            sale.subtotal = 0
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    sale_product = form.save(commit=False)
                    sale_product.sale = sale
                    sale_product.save()
                    sale.subtotal += sale_product.total

            sale.total = sale.subtotal + (sale.subtotal * sale.gst / 100)
            sale.save()
            return redirect('sale-list')
    else:
        sale_form = SaleForm(instance=sale)
        formset = SaleProductFormset(queryset=sale.saleproduct_set.all())

    return render(request, 'sale/sale_form.html', {'sale_form': sale_form, 'formset': formset})


# Sale Delete
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale-list')
    return render(request, 'components/confirm_delete.html', {'object': sale})

def purchase_return(request, purchase_id):
    purchase = get_object_or_404(PurchaseProduct, pk=purchase_id)
    if request.method == 'POST':
        return_quantity = int(request.POST.get('return_quantity'))
        handle_purchase_return(purchase, return_quantity)
        return HttpResponse({'status': 'success', 'message': 'Purchase return processed.'})
    return render(request, 'purchase_return.html', {'purchase': purchase}) # TODO

def sale_return(request, sale_id):
    sale = get_object_or_404(SaleProduct, pk=sale_id)
    if request.method == 'POST':
        return_quantity = int(request.POST.get('return_quantity'))
        handle_sale_return(sale, return_quantity)
        return HttpResponse({'status': 'success', 'message': 'Sale return processed.'})
    return render(request, 'sale_return.html', {'sale': sale}) # TODO
