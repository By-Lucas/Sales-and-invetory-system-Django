from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cart.views.cart_views import cart_update, product_sell, home_carrinho, sell_product


urlpatterns = [
    path('', cart_update, name='add_cart'),
    path('cart', home_carrinho, name='cart'),
    #path('remove/<int:pk>', cart_remove, name='cart-remove'),
    path('vender/<int:pk>', product_sell, name='sell_products'),

]
