# Generated by Django 5.1.3 on 2024-11-19 06:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0003_remove_sale_gst"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="reorder_level",
        ),
        migrations.AlterField(
            model_name="sale",
            name="subtotal",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="sale",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
