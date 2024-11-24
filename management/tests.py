# test.py
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'InventoryManagement.settings'
import django
django.setup()
from django.utils import timezone
from management.models import Vendor, Category, SubCategory, Unit, Product, Purchase, PurchaseProduct, PurchaseReturn
from management.models import PurchaseProductSale, CustomerDetails, Warehouse, Sale, SaleProduct, SaleReturn, Inventory, StockTransfer
import pandas as pd

def create_sample_data():
    
    # SELECT * FROM sqlite_sequence WHERE name='management_vendor';
    # UPDATE sqlite_sequence SET seq = 5 WHERE name = 'management_vendor';

    vendor_df = pd.read_csv('./csv_exports/Vendor_data.csv')
    vendor_df['mobile'] = vendor_df['mobile'].astype(str).str.replace(r'\.0+$', '', regex=True)
    vendor_df = vendor_df[['id','name','address','mobile','status']].drop_duplicates()
    vendors = []
    for index, row in vendor_df.iterrows():
        # Concatenate mobile and address into details
        details = ''
        if pd.notna(row['address']):
            details += row['address']
        if pd.notna(row['mobile']):
            if details:
                details += ' | '  # Add a separator if both address and mobile are present
            details += row['mobile']
        
        # Create Vendor instance
        vendor = Vendor(
            name=row['name'],
            gst='',  # Ensure gst is None if missing
            details=details if details else None,  # Only set details if there's content
            status=True if row['status'] else False  # Handle status as boolean
        )
        vendor.save()