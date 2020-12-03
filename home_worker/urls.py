from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('home/worker/', views.orders,name='home_worker-home'),
    path('profile/worker/', views.profile,name='home_worker-profile'),
    path('orders/worker/', views.OrderHistory, name='home_worker-orders'),
    url(r'^acceptRequest/(?P<req_no>\d+)$', views.acceptRequest, name="acceptRequest"),
    url(r'^acceptRequestAndGroup/(?P<req_no>\d+)$', views.acceptRequestAndGroup, name="acceptRequestAndGroup"),
    url(r'^acceptGroupRequest/(?P<order_id>\d+)$', views.acceptGroupRequest, name="acceptGroupRequest"),
    url(r'^startTime/(?P<order_id>\d+)$', views.startTime, name="startTime"),
    url(r'^endTime/(?P<order_id>\d+)$', views.endTime, name="endTime"),
]