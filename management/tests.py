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

    # vendor_df = pd.read_csv('./csv_exports/Vendor_data.csv')
    # vendor_df['mobile'] = vendor_df['mobile'].astype(str).str.replace(r'\.0+$', '', regex=True)
    # vendor_df = vendor_df[['id','name','address','mobile','status']].drop_duplicates()
    # vendors = []
    # for index, row in vendor_df.iterrows():
    #     # Concatenate mobile and address into details
    #     details = ''
    #     if pd.notna(row['address']):
    #         details += row['address']
    #     if pd.notna(row['mobile']):
    #         if details:
    #             details += ' | '  # Add a separator if both address and mobile are present
    #         details += row['mobile']
        
    #     # Create Vendor instance
    #     vendor = Vendor(
    #         name=row['name'],
    #         gst='',  # Ensure gst is None if missing
    #         details=details if details else None,  # Only set details if there's content
    #         status=True if row['status'] else False  # Handle status as boolean
    #     )
    #     vendor.save()

    # Create categories
    # categories = [
    #     "Clothing",
    #     "Accessories",
    #     "Bags & Luggage",
    #     "Home Decor",
    #     "Jewelry",
    #     "Others"
    # ]

    # # Adding categories
    # for category_name in categories:
    #     category = Category.objects.create(name=category_name)

    # # Create sub-categories (paired with categories)
    # sub_categories = {
    #     1: [  # For "Clothing"
    #         "T-shirt", "Jacket", "Lower", "Track Suit", "Shirt"
    #     ],
    #     2: [  # For "Accessories"
    #         "Hat/Cap", "Bag", "Keychain", "Bottle", "Magnet"
    #     ],
    #     3: [  # For "Bags & Luggage"
    #         "Bag", "Cushion Cover"
    #     ],
    #     4: [  # For "Home Decor"
    #         "Coaster", "Paperweight", "Mugs", "Pot", "Painting", "Fan", "Holder"
    #     ],
    #     5: [  # For "Jewelry"
    #         "Jewelry"
    #     ],
    #     6: [  # For "Others"
    #         "Book"
    #     ]
    # }

    # # Adding sub-categories
    # for category_id, sub_category_names in sub_categories.items():
    #     category = Category.objects.get(id=category_id)
    #     for sub_category_name in sub_category_names:
    #         SubCategory.objects.create(category=category, name=sub_category_name)

    # SELECT * FROM sqlite_sequence WHERE name='management_product';
    # UPDATE sqlite_sequence SET seq = 124 WHERE name = 'management_product';

    # product_df = pd.read_csv('./csv_exports/Product_Cat_SubCat_data_corrected.csv')
    # product_df['unit']=1
    # purchase_df = pd.read_csv('./csv_exports/Purchase_data.csv')
    # product_vendor_df = purchase_df[['product','vendor']].drop_duplicates()
    # merged_df = product_vendor_df.merge(product_df,left_on='product',right_on='id')
    # rows = []
    # new_id = []
    # for index, row in merged_df.iterrows():
    #     print(f"Created Product Name : {row['name']} under Vendor : {row['vendor']} with Details {row['detail']} under Category {row['category_id']} and Sub Category {row['sub_category_id']} having Unit {row['unit']}")
    #     product = Product.objects.create(
    #         vendor=Vendor.objects.get(id=row['vendor']),
    #         name = row['name'],
    #         details = row['detail'],
    #         category=Category.objects.get(id=row['category_id']),
    #         sub_category=SubCategory.objects.get(id=row['sub_category_id']),
    #         unit=Unit.objects.get(id=row['unit'])
    #     )
    #     rows.append(row['id'])
    #     new_id.append(product.id)
    # old_new_mapping = {
    #     "product":rows,
    #     "new_product":new_id
    # }
    # df = pd.DataFrame(old_new_mapping)
    # df.to_csv("./csv_exports/product_mapping.csv",index=False)

    # SELECT * FROM sqlite_sequence WHERE name='management_purchase';
    # UPDATE sqlite_sequence SET seq = 134 WHERE name = 'management_purchase';

    # purchase_df = pd.read_csv('./csv_exports/Purchase_data.csv')
    # product_mapping = pd.read_csv('./csv_exports/product_mapping.csv')
    # purchase_df = purchase_df[['id','product','vendor','qty','price','gst','purchase_date']].drop_duplicates()
    # purchase_df = purchase_df.merge(product_mapping,on='product')
    # purchase_df['purchase_date'] = pd.to_datetime(purchase_df['purchase_date'], utc=True).dt.date
    # purchase_df['total'] = purchase_df['qty'] * purchase_df['price']
    # for index, row in purchase_df.iterrows():
    #     print(f"Created Purchase On : {row['purchase_date']} under Vendor : {row['vendor']} of Total Details {row['total']} for Product {row['product']} having Qty {row['qty']} and Price of {row['price']}")
    #     purchase = PurchaseProduct.objects.create(
    #         purchase = Purchase.objects.create(
    #             purchase_date = row['purchase_date'],
    #             warehouse=Warehouse.objects.get(id=1),
    #             vendor_invoice_number = "OLD SALE ID : " +str(row['id']),
    #             vendor = Vendor.objects.get(id=row['vendor']),
    #             total = row['total']
    #         ),
    #         product = Product.objects.get(id=row['new_product']),
    #         quantity = row['qty'],
    #         price = row['price'],
    #         gst_percent = row['gst'],
    #         total = row['total']
    #     )
    pass