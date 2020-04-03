from django.shortcuts import render, redirect
from .forms import CustomerRegisterForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home_customer-home')
    else:
        form = CustomerRegisterForm()
    return render(request, 'customers/reg_as_customer.html', {'form' : form})