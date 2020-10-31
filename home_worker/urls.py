from django.urls import path
from . import views

urlpatterns = [
    path('home/worker/', views.home,name='home_worker-home'),
    path('about/worker/', views.about,name='home_worker-about'),
]