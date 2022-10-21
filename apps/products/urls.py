from django.urls import path
from products.views.products import (
                                    ProductsView, 
                                    CreateProductView,
                                    ProductDetailView,
                                    DeleteProductView,
                                    EditproductView)


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('cadatrar', CreateProductView.as_view(), name='create-product'),
    path('detalhes/<int:id>', ProductDetailView.as_view(), name='product-detail'),
    path('editar/<int:id>', EditproductView.as_view(), name='product-edit'),
    path('deletar/<int:id>', DeleteProductView.as_view(), name='product-delete'),

]
