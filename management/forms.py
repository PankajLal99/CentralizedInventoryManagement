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
        fields = ['purchase_product', 'margin_percent', 'discount', 'gst_percent']
        labels = {
            'discount':'Discount %',
            'margin_percent':'Margin %',
            'gst_percent':'GST %',

        }
        widgets = {
            'margin_percent': forms.NumberInput(attrs={'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'step': '0.01'}),
            'gst_percent': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        purchase_price = instance.purchase_product.price
        margin = (instance.margin_percent / 100) * purchase_price
        instance.total_margin = margin
        selling_price = purchase_price + margin
        if instance.gst_percent>0:
            selling_gst = (selling_price * (instance.gst_percent/100))
        else:
            selling_gst = 0
        instance.selling_gst = selling_gst
        instance.sub_selling_price = selling_price
        instance.selling_price = selling_price + selling_gst
        if commit:
            instance.save()
        return instance


class SaleForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=255, label='Customer Name')
    gst_number = forms.CharField(max_length=15, required=False, label='GST Number')
    mobile = forms.CharField(max_length=15, label='Mobile')
    details = forms.CharField(widget=forms.Textarea, required=False, label='Details')

    class Meta:
        model = Sale
        fields = ['warehouse','sales_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if editing an existing instance
            self.fields['customer_name'].initial = self.instance.customer.name
            self.fields['gst_number'].initial = self.instance.customer.gst_number
            self.fields['mobile'].initial = self.instance.customer.mobile
            self.fields['details'].initial = self.instance.customer.details

    def save(self, commit=True):
        sale = super().save(commit=False)
        customer, created = CustomerDetails.objects.get_or_create(
            gst_number=self.cleaned_data['gst_number'],
            defaults={
                'name': self.cleaned_data['customer_name'],
                'mobile': self.cleaned_data['mobile'],
                'details': self.cleaned_data['details']
            }
        )
        sale.customer = customer
        if commit:
            sale.save()
        return sale


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
        sub_selling_price = instance.purchase_product_sale.sub_selling_price
        selling_gst = instance.purchase_product_sale.selling_gst
        instance.sub_total = sub_selling_price * instance.quantity
        instance.gst_total = selling_gst * instance.quantity
        instance.total = selling_price * instance.quantity
        if commit:
            instance.save()
            self.update_sale_totals(instance.sale)
        return instance
    
    def update_sale_totals(self, sale):
        # Calculate new subtotal and total
        sale.sub_total = sum(item.sub_total for item in sale.saleproduct_set.all())
        sale.gst_total = sum(item.gst_total for item in sale.saleproduct_set.all())
        sale.total = sum(item.total for item in sale.saleproduct_set.all())
        
        sale.save()

    def delete(self, commit=True):
        instance = self.instance
        sale = instance.sale  # Reference to the Sale instance before deletion
        super().delete(commit)
        # Update totals after deletion
        self.update_sale_totals(sale)
class StockTransferForm(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = ['source_warehouse', 'destination_warehouse', 'product', 'quantity', 'transfer_date', 'remarks']
        widgets = {
            'transfer_date': forms.DateInput(attrs={'type': 'date'}),
        }