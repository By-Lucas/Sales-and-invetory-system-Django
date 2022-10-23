from django import forms

from sales_products.models.sales import SellProduct


class SalesForm(forms.ModelForm):
    class Meta:
        model = SellProduct
        fields = [
            'sold_by',
            'product',
            'quantity',
            'unit_price',
            'amount',
            'order_status'
        ]

