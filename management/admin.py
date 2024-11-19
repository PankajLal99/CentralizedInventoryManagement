from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Vendor, Category, SubCategory, Unit, Product, Purchase, PurchaseProduct, PurchaseReturn
from .models import PurchaseProductSale, CustomerDetails, Warehouse, Sale, SaleProduct, SaleReturn, Inventory, StockTransfer
from .forms import *
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gst', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'gst')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor', 'category', 'sub_category', 'barcode')
    list_filter = ('category', 'sub_category', 'vendor')
    search_fields = ('name', 'barcode', 'vendor__name', 'category__name', 'sub_category__name')

class PurchaseProductInline(admin.TabularInline):
    model = PurchaseProduct
    extra = 1  # Display one empty form by default
    form = PurchaseProductForm

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Check if the field is the foreign key you want to customize
        if db_field.name == "warehouse":
            user = request.user
            if user.groups.filter(name='admin_group').exists():
                queryset = Warehouse.objects.all()
            
            elif user.groups.filter(name='user_group').exists(): 
                queryset = Warehouse.objects.filter(gst_number__isnull=True)
                kwargs["queryset"] = queryset
                if queryset.count()==1:
                    kwargs['initial'] = queryset.first().id
                # Optionally, set the default value if creating a new item
                if request.method == 'GET' and not request.GET.get('id'):
                    kwargs['initial'] = Warehouse.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    inlines = [PurchaseProductInline]
    list_display = ('id', 'purchase_date', 'vendor_invoice_number', 'vendor', 'total')
    list_filter = ('purchase_date', 'vendor')
    search_fields = ('vendor_invoice_number', 'vendor__name')
    
    
@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'gst_percent', 'total')
    list_filter = ('product',)
    search_fields = ('product__name',)
    form = PurchaseProductForm

@admin.register(PurchaseProductSale)
class PurchaseProductSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_product', 'margin_percent','discount','sub_selling_price','gst_percent','selling_gst','selling_price','total_margin')
    list_filter = ('margin_percent', 'selling_gst')
    search_fields = ('purchase_product__product__name',)
    form = PurchaseProductSaleForm

@admin.register(CustomerDetails)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gst_number', 'mobile')
    search_fields = ('name', 'gst_number', 'mobile')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'gst_number')
    search_fields = ('name', 'gst_number', 'mobile')

class SalesProductInline(admin.TabularInline):
    model = SaleProduct
    extra = 1  # Display one empty form by default
    form = SaleProductForm

class CustomerDetailsInline(admin.TabularInline):
    model = CustomerDetails
    extra = 1  # Display one empty form by default
    form = CustomerDetailsForm

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SalesProductInline]
    list_display = ('id', 'warehouse', 'customer', 'customer__gst_number','gst_total','sub_total', 'total','print')
    list_filter = ('warehouse', 'customer')
    search_fields = ('id', 'warehouse__name', 'customer__name')
    form = SaleForm

    def print(self, obj):
        url = reverse('print-invoice', args=[obj.id])  # Replace 'print-invoice' with your actual URL pattern name
        return format_html(f"<a class='btn btn-primary' target='_blank' href='{url}'>Print</a>")

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_product_sale', 'quantity', 'total')
    list_filter = ('purchase_product_sale',)
    search_fields = ('purchase_product_sale__purchase_product__product__name',)
    form = SaleProductForm

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','warehouse', 'product', 'quantity_available', 'reorder_level', 'warehouse', 'last_updated')
    list_filter = ('warehouse', 'product')
    search_fields = ('product__name', 'warehouse__name')


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_warehouse', 'destination_warehouse', 'product', 'quantity', 'transfer_date', 'remarks')
    list_filter = ('source_warehouse', 'destination_warehouse', 'transfer_date')
    search_fields = ('source_warehouse__name', 'destination_warehouse__name', 'product__name')
    # form = StockTransferForm