# Generated by Django 5.1.3 on 2024-11-17 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchaseproduct",
            name="warehouse",
        ),
        migrations.AddField(
            model_name="purchase",
            name="warehouse",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="management.warehouse",
            ),
            preserve_default=False,
        ),
    ]
