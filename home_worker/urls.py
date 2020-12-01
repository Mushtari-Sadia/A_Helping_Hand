from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('home/worker/', views.orders,name='home_worker-home'),
    path('profile/worker/', views.profile,name='home_worker-profile'),
    url(r'^acceptRequest/(?P<req_no>\d+)$', views.acceptRequest, name="acceptRequest"),
    path('orders/', views.OrderHistory, name='home_worker-orders'),
]