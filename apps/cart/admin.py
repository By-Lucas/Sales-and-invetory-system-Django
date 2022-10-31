from django.contrib import admin

from cart.models.cart_models import Cart

class CartAdmim(admin.ModelAdmin):
    list_display = ['id', 'valor_total', 'status']


admin.site.register(Cart, CartAdmim)
