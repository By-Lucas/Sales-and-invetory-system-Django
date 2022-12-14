# Generated by Django 4.1.2 on 2022-11-10 18:49

from django.db import migrations, models
import sales_products.models.sales


class Migration(migrations.Migration):

    dependencies = [
        ('sales_products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellproduct',
            name='code_sale',
            field=models.BigIntegerField(default=sales_products.models.sales.generate_id, editable=False),
        ),
        migrations.AlterField(
            model_name='sellproduct',
            name='quantity',
            field=models.BigIntegerField(blank=True, default=1, null=True),
        ),
    ]
