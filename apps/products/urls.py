from django.urls import path
from products.views.products import (
                                    ProductsView, 
                                    CreateProductView,
                                    ProductDetailView,
                                    DeleteProductView,
                                    EditproductView,
                                    backup_products)


urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('cadatrar', CreateProductView.as_view(), name='create-product'),
    path('detalhes/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('editar/<int:pk>', EditproductView.as_view(), name='product-edit'),
    path('deletar/<int:pk>', DeleteProductView.as_view(), name='product-delete'),
    path('backup', backup_products, name='backup_products')

]
