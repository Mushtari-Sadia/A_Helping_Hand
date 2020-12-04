from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home_customer-home'),
    path('profile/', views.profile, name='home_customer-profile'),
    path('orders/', views.orders, name='home_customer-orders'),
    url(r'^request/(?P<type>\d+)$', views.request_service, name='service_request'),
    url(r'^approveGroup/(?P<order_id>\d+)$', views.approveGroup, name='approveGroup'),
    path('request/electrician/', views.request_electrician, name='electrician_request'),
    url (r'^orders/(?P<rating>\d+)/order(?P<Order_id>\d+)/', views.rate, name='rate'),
]