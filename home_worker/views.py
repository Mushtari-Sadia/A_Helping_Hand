from django.shortcuts import render,redirect
from django.db import connection
from customers.forms import *
# Create your views here.
from workers.views import replaceNoneWithNull
import django_tables2 as tables
from django_tables2 import TemplateColumn
import datetime
from django.contrib import messages

cursor = connection.cursor()


def home(request):
    if 'loggedIn' in request.session and 'user_id' in request.session:
        first_name = ""
        if request.session['user_id'] != -1 : # if a user is logged in
            print(request.session['user_id'])
            if 'user_type' in request.session and request.session['user_type'] == "customer" :
                return redirect('home_customer-home')
            for row in cursor.execute("SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']) ):
                first_name = row[0]
            return render(request, 'home_worker/anotherHome.html',{'loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'], 'first_name' : first_name})
        else :
            return redirect('login')
    return redirect('login')

def profile(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-profile')
        for row in cursor.execute(
                "SELECT FIRST_NAME || ' ' || LAST_NAME,TYPE,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id'])):
            name = row[0]
            type = row[1]
            phone_number = row[2]
            dob = row[3]
            thana = row[4]
            rating = row[5]
            if rating==None :
                rating = 0
            for i in AREA_LIST:
                if int(i[0]) == int(thana):
                    thana = i[1]
                    break

        return render(request, 'home_worker/about.html',{'title' : 'Profile','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],
                                                           'name' : name,'type' : type,'phone_number' : phone_number,
                                                           'dob' : dob,'thana' : thana,
                                                           'rating' : (float(rating)*100)/5})
    else :
        return redirect('home_customer-home')


class CurrentlyAvailableRequests(tables.Table):
    #Order_id = tables.Column(verbose_name='Order ID')
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    customer_address =  tables.Column(verbose_name='Address')
    description = tables.Column(verbose_name='Description')
    request_time = tables.Column(verbose_name='Request Time')
    accept_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequest"  record.req_no  %}">Accept</a>',verbose_name='Accept')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class CurrentlyRunningJobs(tables.Table):
    #Order_id = tables.Column(verbose_name='Order ID')
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    #description = tables.Column(verbose_name='Description')
    start_button = TemplateColumn(
        '<a class="btn btn-dark" href="{% url "startButton"  record.req_no  %}">Start</a>', verbose_name='startButton')
    end_button = TemplateColumn(
        '<a class="btn btn-dark" href="{% url "endButton"  record.req_no  %}">End</a>', verbose_name='endButton')
    #request_time = tables.Column(verbose_name='Request Time')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class JobHistory(tables.Table):
    Order_id = tables.Column(verbose_name='Order ID')
    #customer_name = tables.Column(verbose_name='Customer Name')
    Start_time = tables.Column(verbose_name='Start Time')
    End_time = tables.Column(verbose_name='End Time')
    #request_time = tables.Column(verbose_name='Request Time')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


def orders(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        data = []
        #pending_data = []
        cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if 'user_id' in request.session and request.session['user_id']!=-1:
            worker_id = request.session['user_id']

            print("This is " , worker_id)

            for row in cursor.execute("""
                
SELECT c.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,c.PHONE_NUMBER,c.ADDRESS,a.DESCRIPTION,a.REQ_TIME, TIMEDIFF2( SYSTIMESTAMP, a.REQ_TIME, 'HR'),TIMEDIFF2(SYSTIMESTAMP, a.REQ_TIME, 'min') , a.REQUEST_NO
FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a
WHERE c.THANA_NAME= s.THANA_NAME
AND c.CUSTOMER_ID = ANY(SELECT a.CUSTOMER_ID
			FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
			WHERE a2.Order_id IS NULL AND a2.TYPE= s2.TYPE AND s2.WORKER_ID=""" + str(worker_id) + """)
AND c.CUSTOMER_ID = a.CUSTOMER_ID

AND s.WORKER_ID = """ +  str(worker_id) + """
ORDER BY a.REQ_TIME;"""):
                data_dict = {}
                data_dict['customer_name'] = row[0]
                data_dict['customer_phone_number'] = row[1]
                data_dict['customer_address'] = row[2]
                data_dict['description'] = row[3]
                request_time_hr = row[5]
                request_time_min = row[6]

                data_dict['req_no'] = row[7]

                print("THIS IS BEFORE TABLE ", row[7])

                data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
            #     if float(request_time_hr)>=1 :
            #         data_dict['request_time'] = str(request_time_hr) + " hour(s) ago"
            #     else :
            #         data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                print(data_dict)
                data.append(data_dict)
            #
            # for row in cursor.execute(
            #         "SELECT S.CUSTOMER_ID, S.ORDER_ID, O.ORDER_ID,O.TYPE,O.START_TIME,O.END_TIME " +
            #         "FROM SERVICE_REQUEST S, ORDER_INFO O " +
            #         "WHERE S.ORDER_ID = O.ORDER_ID " +
            #         "AND S.CUSTOMER_ID =" + str(customer_id) + " ORDER BY O.START_TIME;")  :
            #     data_dict = {}
            #     data_dict['Order_id'] = row[2]
            #     data_dict['Type'] = row[3]
            #     data_dict['Start_time'] = row[4].strftime("%m/%d/%Y, %H:%M:%S")
            #     data_dict['End_time'] = row[5].strftime("%m/%d/%Y, %H:%M:%S")
            #     data.append(data_dict)


        availableRequestTable = CurrentlyAvailableRequests(data)
        #pendingtable = PendingTable(pending_data)
        return render(request, 'home_worker/anotherHome.html',{'title' : 'Orders','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'], 'availableRequestTable' : availableRequestTable})
    else :
        return redirect('home_customer-home')


def acceptRequest(request, req_no):

    #print("THIS IS A REQUEST NO", req_no)

    if 'user_id' in request.session and request.session['user_id'] != -1:
        worker_id = request.session['user_id']

    print("Worker_ID = ", worker_id)

    connection.cursor().execute("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID)
                            VALUES( (SELECT TYPE
                            FROM SERVICE_PROVIDER
                            WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) + """);"""
                        )

    # connection.cursor().execute(
    #     """"UPDATE SERVICE_REQUEST
    #         SET ORDER_ID = (SELECT ORDER_ID
    #         FROM ORDER_INFO
    #         WHERE START_TIME IS NULL AND END_TIME IS NULL AND WORKER_ID = """ + str(worker_id) +""")
    #         WHERE REQUEST_NO = """ + str(req_no) + """;"""
    # )

    return redirect('home_worker-home')


def OrderHistory(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        currrentJobs = []
        jobHistory = []
        cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

            print("This is ", worker_id)

            # for row in cursor.execute(
            #     """SELECT
            #
            #        """
            # ):
            #     data_dict = {}
            #     data_dict['customer_name'] = row[0]
            #     data_dict['customer_phone_number'] = row[1]
            #     data_dict['customer_address'] = row[2]
            #     data_dict['description'] = row[3]
            #     request_time_hr = row[5]
            #     request_time_min = row[6]
            #
            #     data_dict['req_no'] = row[7]
            #
            #     print("THIS IS BEFORE TABLE ", row[7])
            #
            #     data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
            #     #     if float(request_time_hr)>=1 :
            #     #         data_dict['request_time'] = str(request_time_hr) + " hour(s) ago"
            #     #     else :
            #     #         data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
            #     print(data_dict)
            #     data.append(data_dict)
            #
            for row in cursor.execute(
                """
                SELECT ORDER_ID, START_TIME, END_TIME
                FROM ORDER_INFO
                WHERE START_TIME IS NOT NULL
                AND END_TIME IS NOT NULL
                AND WORKER_ID = """ + str(worker_id) + """ ;"""
            ) :
                data_dict = {}
                data_dict['Order_id'] = row[0]
                data_dict['Start_time'] = row[1]
                data_dict['End_time'] = row[2]
                # data_dict['Start_time'] = row[4].strftime("%m/%d/%Y, %H:%M:%S")
                # data_dict['End_time'] = row[5].strftime("%m/%d/%Y, %H:%M:%S")
                jobHistory.append(data_dict)

        allJobHistory =JobHistory(data)
        # pendingtable = PendingTable(pending_data)
        return render(request, 'home_worker/orderHistory.html',
                      {'title': 'Orders', 'loggedIn': request.session['loggedIn'],
                       'user_type': request.session['user_type'], 'historyTable': allJobHistory})
    else:
        return redirect('home_customer-home')