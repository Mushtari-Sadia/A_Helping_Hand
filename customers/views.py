from django.shortcuts import render, redirect
from .forms import CustomerRegisterForm
from django.contrib import messages
from django.db import connection as conn
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            date_of_birth = form.cleaned_data.get('birth_year')
            thana_name = form.cleaned_data.get('area_field')
            address = form.cleaned_data.get('address')

            conn.cursor().execute(
                  "INSERT INTO Customer(phone_number,first_name,last_name,password,thana_name,address,date_of_birth)"
                  + " VALUES ('" + phone_number + "','" + first_name + "','" + last_name + "','" + password1 + "','" + thana_name + "','" +
                  address + "'," + "TO_DATE('" + str(date_of_birth) + "', 'YYYY-MM-DD'));")

            messages.success(request, f'Account created for {first_name + " " + last_name}!')
            return redirect('home_customer-home')
    else:
        form = CustomerRegisterForm()
    return render(request, 'customers/reg_as_customer.html', {'form' : form})