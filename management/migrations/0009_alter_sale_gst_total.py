# Generated by Django 5.1.3 on 2024-11-19 10:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0008_rename_gst_percentage_purchaseproductsale_gst_percent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="gst_total",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]