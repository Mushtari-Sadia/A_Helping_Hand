from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home_customer-home'),
    path('about/', views.about,name='home_customer-about'),
]