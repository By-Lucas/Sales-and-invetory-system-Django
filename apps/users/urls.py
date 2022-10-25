from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users.views.user_profile_view import (
                                    ProfileUpdateView, 
                                    SignUpView)


urlpatterns = [
    path('Cadastrar-usuario/', SignUpView.as_view(), name='register_user'),
    path('perfil', ProfileUpdateView.as_view(), name='profile'),
]

# Para carregar STATIC e MIDIAS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)