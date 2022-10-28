from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cart.views.cart_views import cart_update, cart_remove, home_carrinho


urlpatterns = [
    path('', cart_update, name='add_cart'),
    path('cart', home_carrinho, name='cart'),
    path('remove/<int:id>', cart_remove, name='cart-remove'),

]
