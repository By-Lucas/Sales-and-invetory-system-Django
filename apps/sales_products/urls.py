from django.urls import path
from sales_products.views.sales import (
                                    ProductsSoldView,
                                    DeleteProductsSoldView,
                                    sell_produc,
                                    backup_products_sold
                                    )


urlpatterns = [
    path('', sell_produc, name='sell-product'),
    path('todas-as-vendas/', ProductsSoldView.as_view(), name='all_producs_sold'),
    path('deletar<int:pk>', DeleteProductsSoldView.as_view(), name='delete_produc_sold'),
    path('backup/', backup_products_sold, name='backup_products_sold'),

]
