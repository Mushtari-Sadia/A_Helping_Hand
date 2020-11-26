from django.urls import path
from . import views

urlpatterns = [
    path('home/worker/', views.home,name='home_worker-home'),
    path('profile/worker/', views.profile,name='home_worker-profile'),
]