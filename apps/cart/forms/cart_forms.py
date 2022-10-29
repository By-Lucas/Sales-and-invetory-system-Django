from django import forms
from cart.models.cart_models import Cart


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
            'user',
            'produto',
            'valor_produto',
            'desconto',
            'subtotal',
            'quantity',
            'valor_total',
            'status'
        ]