from django.shortcuts import render,redirect
from customers.forms import LoginForm
from django.contrib import messages
from django.db import connection as conn
# Create your views here.

id = -1

def register(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return render(request, 'home_customer/home.html', {'loggedIn': request.session['loggedIn'],'user_type' : request.session['user_type']})
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return render(request, 'home_worker/home.html', {'loggedIn': request.session['loggedIn'],'user_type' : request.session['user_type']})
    return render(request, 'home/register.html')

def logout(request):
    request.session['loggedIn'] = False
    request.session['user_id'] = -1
    request.session['user_type'] = "null"
    messages.success(request,"You have successfully logged out")
    return redirect('login')

def login(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "customer" :
            return redirect('home_customer-home')
        if 'user_type' in request.session and request.session['user_type'] == "worker" :
            return redirect('home_worker-home')
    else :
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                count_cus = 0
                count_wor = 0
                user_type = "null"
                for row in conn.cursor().execute("SELECT CUSTOMER_ID FROM CUSTOMER WHERE PHONE_NUMBER='" + phone_number + "' AND PASSWORD='" + password + "'"):
                    count_cus += 1
                    id = row[0]
                    user_type = "customer"
                    #print_all_sql(customer_id)
                    # TODO LOGIN
                print_all_sql("SELECT CUSTOMER_ID FROM CUSTOMER WHERE PHONE_NUMBER='" + phone_number + "' AND PASSWORD='" + password + "'")
                for row in conn.cursor().execute(
                        "SELECT WORKER_ID FROM SERVICE_PROVIDER WHERE PHONE_NUMBER='" + phone_number + "' AND PASSWORD='" + password + "'"):
                    count_wor += 1
                    id = row[0]
                    user_type = "worker"
                print_all_sql("SELECT WORKER_ID FROM SERVICE_PROVIDER WHERE PHONE_NUMBER='" + phone_number + "' AND PASSWORD='" + password + "'")
                #no one with that phone number or password exists
                if count_cus == 0 and count_wor==0:
                    messages.warning(request, "Invalid phone number or password")
                    form = LoginForm()
                    return render(request, 'home/login.html', {'form': form})
                else :
                    messages.success(request, "Login Successful!")
                    request.session['loggedIn'] = True
                    request.session['user_id'] = id
                    request.session['user_type'] = user_type
                    if user_type == "customer":
                        return redirect('home_customer-home')
                    else :
                        return redirect('home_worker-home')

        else:
            form = LoginForm()
        return render(request, 'home/login.html', {'form': form})

def Team(request):

    return render(request, 'home/Team.html')

def Contact(request):

    return render(request, 'home/Contact.html')


def print_all_sql(sql) :
    f = open("sql.txt", "a")
    f.write("--Query----------\n")
    f.write(sql)
    f.write("\n--EndQuery-------")
    f.write('\n\n')

    f.close()