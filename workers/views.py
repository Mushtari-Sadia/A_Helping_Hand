from django.shortcuts import render, redirect
from customers.forms import *
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
    # If current user goes to register, any registration done by him before will be deleted
    if 'regDone1' in request.session and request.session['regDone1'] == True:
        request.session['regDone1'] = False
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

                    next_page_url = 'register_as_worker_' + str(job_field)
                    return redirect(next_page_url)

            else:
                messages.warning(request, "A user with this phone number already exists!")
                return render(request, 'workers/reg_as_worker.html', {'form': form})

    else:
        form = WorkerRegisterForm()
    return render(request, 'workers/reg_as_worker.html', {'form': form})


def registerElectrician(request):
    # if user has completed first part of registration
    if 'regDone1' in request.session and request.session['regDone1'] == True:
        if request.method == 'POST':
            form = ElectricianRegistrationForm(request.POST)
            if form.is_valid():
                license_info = form.cleaned_data.get('license_info')
                yr_of_experience = form.cleaned_data.get('yr_of_experience')
                qualification = form.cleaned_data.get('qualification')

                worker_id = request.session['user_id']

                if license_info == None :
                    license_info = "Not provided"
                if yr_of_experience == None :
                    yr_of_experience = 0
                if qualification == None :
                    qualification =  "Not provided"


                conn.cursor().execute(
                    "INSERT INTO ELECTRICIAN(WORKER_ID,LICENSE_INFO,YEARS_OF_EXPERIENCE,QUALIFICATION)"
                    + " VALUES ('" + str(worker_id) + "','" + license_info + "','" + str(
                    yr_of_experience) + "','" + qualification + "')")

                name = ""
                for row in conn.cursor().execute(
                        "SELECT (FIRST_NAME || ' ' || LAST_NAME) FROM SERVICE_PROVIDER WHERE WORKER_ID = '" + str(
                            worker_id) + "'"):
                    name = row[0]

                messages.success(request, f'Account created for {name}!')
                request.session['regDone1'] = False
                return redirect('home_worker-home')
        else:
            form = ElectricianRegistrationForm()
        return render(request, 'workers/reg_as_worker.html',
                      {'form': form, 'regSecondPage': request.session['regDone1']})
    else:
        return redirect('register_as_worker')


def registerHomeCleaner(request):
    # if user has completed first part of registration
    if 'regDone1' in request.session and request.session['regDone1'] == True:
        if request.method == 'POST':
            form = HomeCleanerRegistrationForm(request.POST)
            if form.is_valid():
                NID_number = form.cleaned_data.get('NID_number')

                worker_id = request.session['user_id']

                conn.cursor().execute(
                    "INSERT INTO HOME_CLEANER(WORKER_ID,NID )"
                    + " VALUES ('" + str(worker_id) + "','" + NID_number + "')")

                name = ""
                for row in conn.cursor().execute(
                        "SELECT (FIRST_NAME || ' ' || LAST_NAME) FROM SERVICE_PROVIDER WHERE WORKER_ID = '" + str(
                            worker_id) + "'"):
                    name = row[0]

                messages.success(request, f'Account created for {name}!')
                request.session['regDone1'] = False
                return redirect('home_worker-home')
        else:
            form = HomeCleanerRegistrationForm()
        return render(request, 'workers/reg_as_worker.html',
                      {'form': form, 'regSecondPage': request.session['regDone1']})
    else:
        return redirect('register_as_worker')


def registerPestControlService(request):
    # if user has completed first part of registration
    if 'regDone1' in request.session and request.session['regDone1'] == True:
        if request.method == 'POST':
            form = PestControlServiceRegistrationForm(request.POST)
            if form.is_valid():
                license_info = form.cleaned_data.get('license_info')
                chemical_info = form.cleaned_data.get('chemical_info')

                worker_id = request.session['user_id']

                conn.cursor().execute(
                    "INSERT INTO PEST_CONTROL(WORKER_ID,LICENSE_INFO,CHEMICAL_INFO )"
                    + " VALUES ('" + str(worker_id) + "','" + license_info + "','" + chemical_info + "')")

                name = ""
                for row in conn.cursor().execute(
                        "SELECT (FIRST_NAME || ' ' || LAST_NAME) FROM SERVICE_PROVIDER WHERE WORKER_ID = '" + str(
                            worker_id) + "'"):
                    name = row[0]

                messages.success(request, f'Account created for {name}!')
                request.session['regDone1'] = False
                return redirect('home_worker-home')
        else:
            form = PestControlServiceRegistrationForm()
        return render(request, 'workers/reg_as_worker.html',
                      {'form': form, 'regSecondPage': request.session['regDone1']})
    else:
        return redirect('register_as_worker')


def registerPlumber(request):
    # if user has completed first part of registration
    if 'regDone1' in request.session and request.session['regDone1'] == True:
        if request.method == 'POST':
            form = PlumberRegistrationForm(request.POST)
            if form.is_valid():
                yr_of_experience = form.cleaned_data.get('yr_of_experience')

                worker_id = request.session['user_id']

                conn.cursor().execute(
                    "INSERT INTO PLUMBER(WORKER_ID, YEARS_OF_EXPERIENCE )"
                    + " VALUES ('" + str(worker_id) + "','" + str(
                        yr_of_experience) + "')")

                name = ""
                for row in conn.cursor().execute(
                        "SELECT (FIRST_NAME || ' ' || LAST_NAME) FROM SERVICE_PROVIDER WHERE WORKER_ID = '" + str(
                            worker_id) + "'"):
                    name = row[0]

                messages.success(request, f'Account created for {name}!')
                request.session['regDone1'] = False
                return redirect('home_worker-home')
        else:
            form = PlumberRegistrationForm()
        return render(request, 'workers/reg_as_worker.html',
                      {'form': form, 'regSecondPage': request.session['regDone1']})
    else:
        return redirect('register_as_worker')