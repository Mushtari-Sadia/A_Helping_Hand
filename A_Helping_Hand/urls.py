"""A_Helping_Hand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from customers import views as customer_views
from home import views as home_views
from users import views as user_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',home_views.register, name = 'register'),
    path('register_customer/',customer_views.register, name = 'register_as_customer'),
    path('', include('home_customer.urls')),
    path('register/',user_views.register, name = 'register'),
    path('', include('home_consumer.urls')),

]
