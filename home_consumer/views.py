from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home_consumer/home.html')

def about(request):
    return render(request, 'home_consumer/about.html',{'title' : 'About'})

