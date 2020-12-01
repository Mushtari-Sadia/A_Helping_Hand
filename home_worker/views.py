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
            return render(request, 'home_worker/home.html',{'loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'], 'first_name' : first_name})
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

        return render(request, 'home_worker/about.html',{'title' : 'Profile','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],
                                                           'name' : name,'type' : type,'phone_number' : phone_number,
                                                           'dob' : dob,'thana' : thana,
                                                           'rating' : (float(rating)*100)/5})
    else :
        return redirect('home_customer-home')


class CurrentlyAvailableRequests(tables.Table):
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    customer_address =  tables.Column(verbose_name='Address')
    description = tables.Column(verbose_name='Description')
    request_time = tables.Column(verbose_name='Request Time')
    accept_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequest"  record.req_no  %}">Accept</a>',verbose_name='Accept')

    class Meta:
        template_name = "django_tables2/bootstrap.html"



def orders(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        for row in cursor.execute(
                "SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id'])):
            first_name = row[0]

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
            AND c.CUSTOMER_ID = ANY(SELECT a2.CUSTOMER_ID
                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id) +""")
            AND a.CUSTOMER_ID = c.CUSTOMER_ID
            AND a.REQUEST_NO = ANY(SELECT a2.REQUEST_NO
                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id) +""")
            AND s.WORKER_ID="""+str(worker_id) +""";"""):
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
                if float(request_time_hr)>=1 :
                    data_dict['request_time'] = str(request_time_hr) + " hour(s) ago"
                else :
                    data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                # print("data_dict",data_dict)
                data.append(data_dict)
            print("all data", data)
            availableRequestTable = CurrentlyAvailableRequests(data)
            # pendingtable = PendingTable(pending_data)
            empty = False
            if len(data) == 0 :
                empty = True
                return render(request, 'home_worker/home.html',{'title' : 'Home','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],'first_name': first_name, 'empty' : empty})
            else :
                return render(request, 'home_worker/home.html',{'title' : 'Home','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],'first_name': first_name, 'empty' : empty, 'availableRequestTable' : availableRequestTable})
    else :
        return redirect('home_customer-home')


def acceptRequest(request, req_no):

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

        # print("Worker_ID = ", worker_id)

        connection.cursor().execute("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID,REQUEST_NO)
                                VALUES( (SELECT TYPE
                                FROM SERVICE_PROVIDER
                                WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) +""",""" + str(req_no) +  """);"""
                            )

        connection.cursor().execute(
            """UPDATE SERVICE_REQUEST
                SET ORDER_ID = (SELECT ORDER_ID
                FROM ORDER_INFO
                WHERE REQUEST_NO = """ + str(req_no) +""")
                WHERE REQUEST_NO = """ + str(req_no) + """;"""
        )

        return redirect('home_worker-home')
    else :
        return redirect('home_customer-home')


class CurrentlyRunningJobs(tables.Table):
    customer_name = tables.Column(verbose_name='Name')
    customer_phone = tables.Column(verbose_name='Phone Number')
    customer_address = tables.Column(verbose_name='Address')
    Order_id = tables.Column(verbose_name='Order ID')
    start_button = TemplateColumn(
        "{% if record.Start_time %} <p>{{record.Start_time}}</p> {%else%}<a class='btn btn-dark' href='{% url 'startTime' record.Order_id %}'>Start</a>{%endif%}",
        verbose_name='Start Time')
    end_button = TemplateColumn(
        '<a class="btn btn-dark" href="{% url "endTime" record.Order_id %}">End</a>', verbose_name='End Time')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class JobHistory(tables.Table):
    customer_name = tables.Column(verbose_name='Name')
    customer_phone = tables.Column(verbose_name='Phone Number')
    customer_address = tables.Column(verbose_name='Address')
    Order_id = tables.Column(verbose_name='Order ID')
    Start_time = tables.Column(verbose_name='Start Time')
    End_time = tables.Column(verbose_name='End Time')
    Rating = TemplateColumn(verbose_name='Rate Customer',template_name='home_customer/rating.html')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


def OrderHistory(request):
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-orders')

        currentJobs = []
        empcurrentjobs = False
        jobHistory = []
        empjobhistory = False

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

            for row in connection.cursor().execute(
                """
                SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                FROM CUSTOMER C,ORDER_INFO O
                WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
												FROM SERVICE_REQUEST SR
												WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                AND O.START_TIME IS NOT NULL AND O.END_TIME IS NOT NULL AND O.ORDER_ID IS NOT NULL
                AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+ str(worker_id) +""")

												;"""
            ) :

                data_dict = {}
                data_dict['customer_name'] = row[0]
                data_dict['customer_phone'] = row[1]
                data_dict['customer_address'] = row[2]

                data_dict['Order_id'] = row[3]
                start_time = row[4]
                end_time = row[5]
                if start_time != None:
                    start_time = start_time.strftime("%m/%d/%Y, %H:%M:%S")
                if end_time != None:
                    end_time = end_time.strftime("%m/%d/%Y, %H:%M:%S")
                data_dict['Start_time'] = start_time
                data_dict['End_time'] = end_time

                jobHistory.append(data_dict)

            for row in connection.cursor().execute(
                        """
                        SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                        FROM CUSTOMER C,ORDER_INFO O
                        WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                                        FROM SERVICE_REQUEST SR
                                                        WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID=""" + str(
                            worker_id) + """))
                            AND O.ORDER_ID IS NOT NULL AND O.END_TIME IS NULL
                            AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID=""" + str(
                            worker_id) + """)

            												;"""
                ):

                    data_dict = {}
                    data_dict['customer_name'] = row[0]
                    data_dict['customer_phone'] = row[1]
                    data_dict['customer_address'] = row[2]

                    data_dict['Order_id'] = row[3]
                    start_time = row[4]
                    end_time = row[5]
                    if start_time != None:
                        start_time = start_time.strftime("%m/%d/%Y, %H:%M:%S")
                    if end_time != None:
                        end_time = end_time.strftime("%m/%d/%Y, %H:%M:%S")
                    data_dict['Start_time'] = start_time
                    data_dict['End_time'] = end_time

                    currentJobs.append(data_dict)

        if len(jobHistory) == 0 :
            empjobhistory = True
        if len(currentJobs) == 0:
            empcurrentjobs = True

        allJobHistory = JobHistory(jobHistory)
        currenttable = CurrentlyRunningJobs(currentJobs)

        return render(request, 'home_worker/orderHistory.html', {'title': 'Home', 'loggedIn': request.session['loggedIn'],
                                                         'user_type': request.session['user_type'],'currenttable' : currenttable, 'historytable' : allJobHistory,'empcurrenttable' : empcurrentjobs,'emphistoryTable' : empjobhistory})
    else:
        return redirect('home_customer-home')



def startTime(request,order_id) :
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')
        # cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS')
        connection.cursor().execute("""
        UPDATE ORDER_INFO
        SET START_TIME = SYSTIMESTAMP
        WHERE ORDER_ID = """+ str(order_id) +""";""")
        return redirect('home_worker-orders')
    else:
        return redirect('login')

def endTime(request,order_id) :
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')
        # cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS')
        connection.cursor().execute("""
        UPDATE ORDER_INFO
        SET END_TIME = SYSTIMESTAMP
        WHERE ORDER_ID = """+ str(order_id) +""";""")
        return redirect('home_worker-orders')
    else:
        return redirect('login')
