from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('produtos/', include('inventory.urls')),
    path('produtos/', include('products.urls')),
    path('vendas/', include('sales_products.urls')),
    path('usuario/', include('users.urls'))
]


# Para carregar STATIC e MIDIAS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)