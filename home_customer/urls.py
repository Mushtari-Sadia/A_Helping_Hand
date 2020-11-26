from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home_customer-home'),
    path('about/', views.about, name='home_customer-about'),
    path('orders/', views.orders, name='home_customer-orders'),
    path('request/', views.request_service, name='service_request'),
    path('request/electrician/', views.request_electrician, name='electrician_request'),
]