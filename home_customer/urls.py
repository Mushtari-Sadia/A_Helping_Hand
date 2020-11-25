from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name='home_customer-home'),
    path('about/', views.about,name='home_customer-about'),
    path('orders/', views.orders,name='home_customer-orders'),
]