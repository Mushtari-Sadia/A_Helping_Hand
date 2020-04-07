from django.shortcuts import render,redirect
from customers.forms import LoginForm
from django.contrib import messages
from django.db import connection as conn
# Create your views here.
customer_id = -1

def register(request):
    return render(request, 'home/register.html')

def logout(request):
    request.session['loggedIn'] = False
    request.session['user_id'] = -1
    messages.success(request,"You have successfully logged out")
    return redirect('register')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            count = 0
            for row in conn.cursor().execute("SELECT CUSTOMER_ID FROM CUSTOMER WHERE PHONE_NUMBER='" + phone_number + "' AND PASSWORD='" + password + "'"):
                count += 1
                customer_id = row[0]
                #print(customer_id)
            if count == 0 :
                messages.warning(request, "Invalid phone number or password")
                form = LoginForm()
                return render(request, 'home/login.html', {'form': form})
            else :
                messages.success(request, "Login Successful!")
                #TODO SADIA 1 : DEFINITION IS HERE ONLY.SO IF NOT LOGGED IN, GIVES KEYERROR. FIX THIS
                request.session['loggedIn'] = True
                request.session['user_id'] = customer_id
                return render(request,'home_customer/home.html',{'loggedIn' : request.session['loggedIn']})

    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})

