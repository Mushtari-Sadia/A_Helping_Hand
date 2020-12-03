from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.db import connection as conn
# Create your views here.


def register(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
            return render(request, 'home_customer/home.html', {'loggedIn': request.session['loggedIn'],'user_type' : request.session['user_type']})
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            date_of_birth = form.cleaned_data.get('birth_year')
            thana_name = form.cleaned_data.get('area_field')

            address = form.cleaned_data.get('address')

            for i in AREA_LIST:
                if int(i[0]) == int(thana_name):
                    thana_name = i[1]
                    break

            count_cus = 0
            count_wor = 0

            print("SELECT * FROM CUSTOMER WHERE PHONE_NUMBER = '" + phone_number + "'")

            for row in conn.cursor().execute("SELECT * FROM CUSTOMER WHERE PHONE_NUMBER = '" + phone_number + "'"):
                count_cus += 1

            print( "SELECT * FROM SERVICE_PROVIDER WHERE PHONE_NUMBER = '" + phone_number + "'")

            for row in conn.cursor().execute(
                    "SELECT * FROM SERVICE_PROVIDER WHERE PHONE_NUMBER = '" + phone_number + "'"):
                count_wor += 1
            # if user has entered a phone number that no one has entered before
            if count_cus == 0 and count_wor == 0:
                conn.cursor().execute(
                    "INSERT INTO Customer(phone_number,first_name,last_name,password,thana_name,address,date_of_birth)"
                    + " VALUES ('" + phone_number + "','" + first_name + "','" + last_name + "','" + password1 + "','" + thana_name + "','" +
                    address + "'," + "TO_DATE('" + str(date_of_birth) + "', 'YYYY-MM-DD'))")

                print("INSERT INTO Customer(phone_number,first_name,last_name,password,thana_name,address,date_of_birth)"
                    + " VALUES ('" + phone_number + "','" + first_name + "','" + last_name + "','" + password1 + "','" + thana_name + "','" +
                    address + "'," + "TO_DATE('" + str(date_of_birth) + "', 'YYYY-MM-DD'))")

                messages.success(request, f'Account created for {first_name + " " + last_name}!')
                return redirect('home_customer-home')
            else :
                messages.warning(request,"A user with this phone number already exists!")
                return render(request, 'customers/reg_as_customer.html', {'form': form})

    else:
        form = CustomerRegisterForm()
    return render(request, 'customers/reg_as_customer.html', {'form' : form})