from django.shortcuts import render, redirect
from customers.forms import WorkerRegisterForm
from django.contrib import messages
# Create your views here.

# TODO 2 : complete worker registration form same as customer registration form, check customers/views.py
def register(request):
    if request.method == 'POST':
        form = WorkerRegisterForm(request.POST)
        if form.is_valid():
            return redirect('home_worker-home')
    else:
        form = WorkerRegisterForm()
    return render(request, 'workers/reg_as_worker.html', {'form' : form})