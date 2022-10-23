from django.urls import path
from sales_products.views.sales import (
                                    SellProductView,
                                    sell_produc
                                    )


urlpatterns = [
    path('', sell_produc, name='sell-product'),
]
