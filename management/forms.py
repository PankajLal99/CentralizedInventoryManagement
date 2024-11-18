from django import forms
from .models import *

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'gst', 'details', 'status']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendor', 'name', 'details', 'image', 'category', 'sub_category', 'unit']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['vendor','warehouse','vendor_invoice_number', 'purchase_date', 'total']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PurchaseProductForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['product','quantity', 'price', 'gst_percent']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'gst_percent': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean(self):
        """Custom clean method to ensure fields are valid."""
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')

        # Validate that quantity and price are provided and valid
        if quantity is None or price is None:
            raise forms.ValidationError("Both Quantity and Price are required.")
        
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")

        return cleaned_data

    def save(self, commit=True):
        """Override save to calculate total and ensure no blank fields."""
        instance = super().save(commit=False)

        # Ensure quantity and price are not None before calculating total
        instance.quantity = instance.quantity or 0  # Default to 0 if None
        instance.price = instance.price or 0  # Default to 0 if None
        instance.total = instance.quantity * instance.price

        # Prevent saving if the form is blank (e.g., added accidentally)
        if instance.quantity == 0 and instance.price == 0:
            return None  # Don't save this instance
        
        if commit:
            instance.save()
        return instance

# Inline formset for PurchaseProduct
PurchaseProductFormset = forms.modelformset_factory(
    PurchaseProduct,
    form=PurchaseProductForm,
    extra=5,  # Display one empty form by default
    can_delete=True  # Optionally allow deletion of products
)

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = CustomerDetails
        fields = ['name', 'gst_number', 'mobile', 'details']

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'gst_number', 'mobile', 'details']

class PurchaseProductSaleForm(forms.ModelForm):
    class Meta:
        model = PurchaseProductSale
        fields = ['purchase_product', 'margin_percent', 'discount', 'selling_gst']
        widgets = {
            'margin_percent': forms.NumberInput(attrs={'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'step': '0.01'}),
            'selling_gst': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        purchase_price = instance.purchase_product.price
        margin = (instance.margin_percent / 100) * purchase_price
        instance.total_margin = margin
        selling_price = purchase_price + margin - (instance.discount or 0)
        if instance.selling_gst>0:
            instance.selling_price = selling_price + (selling_price * (instance.selling_gst/100))
        else:
            instance.selling_price = selling_price
        if commit:
            instance.save()
        return instance


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['warehouse', 'customer']


class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['purchase_product_sale', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        selling_price = instance.purchase_product_sale.selling_price
        instance.total = selling_price * instance.quantity
        if commit:
            instance.save()
        return instance
    
class StockTransferForm(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = ['source_warehouse', 'destination_warehouse', 'product', 'quantity', 'transfer_date', 'remarks']
        widgets = {
            'transfer_date': forms.DateInput(attrs={'type': 'date'}),
        }