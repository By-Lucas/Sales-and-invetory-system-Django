# Generated by Django 4.1.2 on 2022-10-23 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_products', '0011_balance_amoun_week_balance_amount_day_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='amoun_week',
            new_name='amount_week',
        ),
    ]