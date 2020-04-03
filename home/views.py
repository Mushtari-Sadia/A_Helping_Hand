from django.shortcuts import render,redirect

# Create your views here.


def register(request):
    return render(request, 'home/register.html')


def login(request):
    return render(request,'home/login.html')