from django.urls import path
from core.views.home import HomeView, LoginView, LogoutView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
