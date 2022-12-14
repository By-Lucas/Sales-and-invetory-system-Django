# Generated by Django 4.1.2 on 2022-11-10 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sales_products.models.sales


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('amount_day', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('amount_week', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('amount_month', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('date_order', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Saldo',
                'verbose_name_plural': 'Saldos',
                'db_table': 'balance',
                'ordering': ('-date_order',),
            },
        ),
        migrations.CreateModel(
            name='SellProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_sale', models.IntegerField(default=sales_products.models.sales.generate_id, editable=False)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=9, null=True)),
                ('date_sale', models.DateTimeField(auto_now_add=True)),
                ('cart_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('sold_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Produtos vendidos',
                'verbose_name_plural': 'Produtos vendidos',
                'db_table': 'sales',
                'ordering': ('-date_sale',),
            },
        ),
    ]
