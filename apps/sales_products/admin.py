from django.contrib import admin
from sales_products.models.balance import Balance
from sales_products.models.sales import SellProduct


class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ('sold_by', )
    list_display = ['cart_product', 'quantity', 'amount', 'date_sale']

    def save_model(self, request, obj, form, change):
        user_ = request.user
        obj.sold_by = user_
        super(SaleAdmin, self).save_model(request, obj, form, change)

admin.site.register(SellProduct, SaleAdmin)


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date_update', 'date_order')