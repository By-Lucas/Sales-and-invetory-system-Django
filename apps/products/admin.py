from django.contrib import admin
from products.models.products import Products

#admin.site.register(Products)


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by_user', )
    list_display = ('name', 'code', 'value', 'status', 'date_create')
    list_editable = ('value',)
    list_filter = ( 'name', 'value')

    def save_model(self, request, obj, form, change):
        user_ = request.user
        obj.created_by_user = user_
        super(ProductAdmin, self).save_model(request, obj, form, change)


admin.site.register(Products, ProductAdmin)
