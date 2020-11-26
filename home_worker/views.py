from django.shortcuts import render,redirect
from django.db import connection
# Create your views here.

cursor = connection.cursor()

def home(request):
    if 'loggedIn' in request.session and 'user_id' in request.session:
        first_name = ""
        if request.session['user_id'] != -1 : # if a user is logged in
            print(request.session['user_id'])
            if 'user_type' in request.session and request.session['user_type'] == "customer" :
                return redirect('home_customer-home')
            for row in cursor.execute("SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']) ):
                first_name = row[0]
            return render(request, 'home_worker/home.html',{'loggedIn' : request.session['loggedIn'], 'first_name' : first_name})
        else :
            return redirect('login')
    return redirect('login')

def profile(request):
    if 'loggedIn' in request.session:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_worker-profile')
        return render(request, 'home_worker/about.html',{'title' : 'profile','loggedIn' : request.session['loggedIn']})
    else :
        return render(request, 'home_worker/about.html', {'title': 'profile'})

