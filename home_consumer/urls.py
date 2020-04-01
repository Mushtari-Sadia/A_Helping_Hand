from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home_consumer-home'),
    path('about/', views.about,name='home_consumer-about'),
]