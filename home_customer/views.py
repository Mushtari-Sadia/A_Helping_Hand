from django.shortcuts import render,redirect
from django.db import connection
# Create your views here.

cursor = connection.cursor()

def home(request):
    if 'loggedIn' in request.session and 'user_id' in request.session:
        first_name = ""
        if request.session['user_id'] != -1 : # if a user is logged in
            print(request.session['user_id'])
            for row in cursor.execute("SELECT FIRST_NAME FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id']) ):
                first_name = row[0]
            return render(request, 'home_customer/home.html',{'loggedIn' : request.session['loggedIn'], 'first_name' : first_name})
        else :
            return redirect('login')
    return redirect('login')

def about(request):
    if 'loggedIn' in request.session:
        return render(request, 'home_customer/about.html',{'title' : 'About','loggedIn' : request.session['loggedIn']})
    else :
        return render(request, 'home_customer/about.html', {'title': 'About'})

