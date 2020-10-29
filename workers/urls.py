from django.urls import path
from . import views

urlpatterns = [

    path('register/worker/', views.register, name='register_as_worker'),
    path('register/worker/electrician/', views.registerElectrician, name='register_as_worker_1'),
    path('register/worker/home_cleaner/', views.registerHomeCleaner, name='register_as_worker_2'),
    path('register/worker/pest_control_service/', views.registerPestControlService, name='register_as_worker_3'),
    path('register/worker/plumber/', views.registerPlumber, name='register_as_worker_4'),
]