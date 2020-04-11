from django.urls import path
from . import views

urlpatterns = [

    path('register/worker/', views.register, name='register_as_worker'),
    path('register/worker/electrician/', views.registerElectrician, name='register_as_worker_1'),
]