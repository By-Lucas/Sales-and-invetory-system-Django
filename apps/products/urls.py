from django.urls import path
from products.views.products import (
                                    ProductsView, 
                                    CreateProductView)


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('cadatrar/', CreateProductView.as_view(), name='create-product'),
]
