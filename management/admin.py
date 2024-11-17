from django.contrib import admin
from .models import Vendor, Category, SubCategory, Unit, Product, Purchase, PurchaseProduct, PurchaseReturn
from .models import PurchaseProductSale, CustomerDetails, Warehouse, Sale, SaleProduct, SaleReturn, Inventory, StockTransfer


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

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseProductInline]
    list_display = ('id', 'purchase_date', 'vendor_invoice_number', 'vendor', 'total')
    list_filter = ('purchase_date', 'vendor')
    search_fields = ('vendor_invoice_number', 'vendor__name')


@admin.register(PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'gst_percent', 'total')
    list_filter = ('product',)
    search_fields = ('product__name',)


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'product', 'quantity', 'reason', 'return_date')
    list_filter = ('return_date', 'product')
    search_fields = ('product__name', 'reason')


@admin.register(PurchaseProductSale)
class PurchaseProductSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_product', 'margin_percent', 'total_margin', 'discount', 'selling_price', 'selling_gst')
    list_filter = ('margin_percent', 'selling_gst')
    search_fields = ('purchase_product__product__name',)


@admin.register(CustomerDetails)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gst_number', 'mobile')
    search_fields = ('name', 'gst_number', 'mobile')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'gst_number')
    search_fields = ('name', 'gst_number', 'mobile')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'customer', 'customer__gst_number', 'subtotal', 'total')
    list_filter = ('warehouse', 'customer')
    search_fields = ('id', 'warehouse__name', 'customer__name')


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_product_sale', 'quantity', 'total')
    list_filter = ('purchase_product_sale',)
    search_fields = ('purchase_product_sale__purchase_product__product__name',)


@admin.register(SaleReturn)
class SaleReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity', 'reason', 'return_date')
    list_filter = ('return_date', 'product')
    search_fields = ('product__name', 'reason')


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
