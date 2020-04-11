from django.shortcuts import render, redirect
from customers.forms import WorkerRegisterForm,ElectricianRegistrationForm
from django.contrib import messages
from django.db import connection as conn
# Create your views here.


# basic_fields = {
#                 'phone_number' : phone_number,
#                 'first_name' : first_name,
#                 'last_name' : last_name,
#                 'password1' : password1,
#                 'date_of_birth' : date_of_birth,
#                 'thana_name' : thana_name,
#                 'address' : address,
#             }


phone_number = ""
first_name = ""
last_name = ""
password1 = ""
date_of_birth = ""
thana_name = ""
address = ""



# TODO SADIA 2 : complete worker registration form
def register(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
            return render(request, 'home_worker/home.html', {'loggedIn': request.session['loggedIn']})
    if request.method == 'POST':
        form = WorkerRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            date_of_birth = form.cleaned_data.get('birth_year')
            thana_name = form.cleaned_data.get('area_field')
            address = form.cleaned_data.get('address')

            count = 0
            for row in conn.cursor().execute(
                    "SELECT * FROM SERVICE_PROVIDER WHERE PHONE_NUMBER = '" + phone_number + "'"):
                count += 1
            # if user has entered a phone number that no one has entered before
            if count == 0:
                conn.cursor().execute(
                    "INSERT INTO SERVICE_PROVIDER(phone_number,first_name,last_name,password,thana_name,address,date_of_birth)"
                    + " VALUES ('" + phone_number + "','" + first_name + "','" + last_name + "','" + password1 + "','" + thana_name + "','" +
                    address + "'," + "TO_DATE('" + str(date_of_birth) + "', 'YYYY-MM-DD'))")
                for row in conn.cursor().execute(
                        "SELECT WORKER_ID FROM SERVICE_PROVIDER WHERE PHONE_NUMBER = '" + phone_number + "'"):
                    worker_id = row[0]
                    # if the person has completed this part of the registration
                    request.session['regDone1'] = True
                    request.session['user_id'] = worker_id

                    # forms = [
                    #     None,
                    #     ElectricianRegistrationForm(),
                    # ]

                    job_field = form.cleaned_data.get('job_field')
                    # template_name = "workers/reg_as_worker_" + str(job_field) + ".html"
                    # return render(request,template_name,{'form' : forms[job_field]})

                    next_page_url = "reg_as_worker_" + str(job_field)
                    return redirect('register_as_worker_1')

            else:
                messages.warning(request, "A user with this phone number already exists!")
                return render(request, 'workers/reg_as_worker.html', {'form': form})

    else:
        form = WorkerRegisterForm()
    return render(request, 'workers/reg_as_worker.html', {'form' : form})



def registerElectrician(request):
    #if user has completed first part of registration
    if 'regDone1' in request.session and request.session['regDone1'] == True :
        if request.method == 'POST' :
            form = ElectricianRegistrationForm(request.POST)
            if form.is_valid():
                license_info = form.cleaned_data.get('license_info')
                yr_of_experience = form.cleaned_data.get('yr_of_experience')
                qualification = form.cleaned_data.get('qualification')
                print("@@@@@@@@@@@first name is " + first_name)

                worker_id = request.session['user_id']

                conn.cursor().execute(
                    "INSERT INTO ELECTRICIAN(WORKER_ID,LICENSE_INFO,YEARS_OF_EXPERIENCE,QUALIFICATION)"
                    + " VALUES ('" + str(worker_id) + "','" + license_info + "','" + str(yr_of_experience) + "','" + qualification + "')")

                messages.success(request, f'Account created for {first_name + " " + last_name}!')
                return redirect('home_worker-home')
        else :
            form = ElectricianRegistrationForm()
        return render(request,'workers/reg_as_worker_1.html',{'form' : form})
    else :
        return redirect('register_as_worker')