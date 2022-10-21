from django.urls import path
from core.views.home import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
