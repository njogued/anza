# Generated by Django 4.2.10 on 2024-09-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_quantity_cart_total_price_remove_cart_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
