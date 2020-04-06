from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'home_customer/home.html',{'loggedIn' : request.session['loggedIn']})

def about(request):
    return render(request, 'home_customer/about.html',{'title' : 'About','loggedIn' : request.session['loggedIn']})

