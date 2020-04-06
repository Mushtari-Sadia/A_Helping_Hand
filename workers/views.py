from django.shortcuts import render, redirect
from customers.forms import WorkerRegisterForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = WorkerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}!')
            return redirect('home_worker-home')
    else:
        form = WorkerRegisterForm()
    return render(request, 'workers/reg_as_worker.html', {'form' : form})