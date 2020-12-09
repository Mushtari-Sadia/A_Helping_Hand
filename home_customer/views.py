from django.shortcuts import render,redirect
from django.db import connection
from customers.forms import *
from workers.views import replaceNoneWithNull
import django_tables2 as tables
from django_tables2 import TemplateColumn
import datetime
from django.contrib import messages
from home.views import *
# Create your views here.
cursor = connection.cursor()

def home(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        first_name = ""
        if 'user_id' in request.session and request.session['user_id'] != -1 : # if a user is logged in
            # print_all_sql(request.session['user_id'])
            if 'user_type' in request.session and request.session['user_type'] == "worker" :
                return redirect('home_worker-home')
            for row in cursor.execute("SELECT FIRST_NAME FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id']) ):
                first_name = row[0]
            print_all_sql("SELECT FIRST_NAME FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id']))
            return render(request, 'home_customer/home.html',{'loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'], 'first_name' : first_name})
        else :
            return redirect('login')
    else :
        return redirect('login')

def profile(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-profile')
        for row in cursor.execute(
                "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING,RATED_BY FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id'])):
            name = row[0]
            phone_number = row[1]
            dob = row[2]
            thana = row[3]
            rating = row[4]
            rated_by = row[5]
            if rating == None or rated_by == None:
                rating = 0
                rated_by = 0

        print_all_sql("SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING,RATED_BY FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id']))

        return render(request, 'home_customer/about.html',{'title' : 'Profile','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],
                                                           'name' : name,'phone_number' : phone_number,
                                                           'dob' : dob,'thana' : thana,
                                                           'rating' : (float(rating)*100)/5,
                                                            'rated_by' : int(rated_by)})
    else :
        return redirect('home_customer-home')


class OrderTable(tables.Table):
    Order_id = tables.Column(verbose_name='Order ID')
    Type = tables.Column(verbose_name='Service Provider')
    Start_time = tables.Column(verbose_name='Start Time')
    End_time = tables.Column(verbose_name='End Time')
    Payment = tables.Column(verbose_name='Payment Tk.')
    Rating = TemplateColumn(verbose_name='Rate Service',template_name='home_customer/rating.html')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class GroupTable(tables.Table):
    order_id = tables.Column(verbose_name='Order ID')
    Team_leader_name = tables.Column(verbose_name='Requested By')
    Type = tables.Column(verbose_name='Service')
    worker_contact_no = tables.Column(verbose_name='Contact No.')
    Estimated_payment = tables.Column(verbose_name='Estimated payment')
    approve_button = TemplateColumn('<a class="btn btn-dark" href="{% url "approveGroup"  record.order_id  %}">Approve</a>',verbose_name='Approve Request')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class PendingTable(tables.Table):
    Type = tables.Column(verbose_name='Service Provider')
    Description = tables.Column(verbose_name='Description')
    Request_time = tables.Column(verbose_name='Request Time')

    class Meta:
        template_name = "django_tables2/bootstrap.html"



def orders(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-home')

        data = []
        empty = False
        pending_data = []
        emptyPending = False
        group_data = []
        emptyGrp = False
        cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if 'user_id' in request.session and request.session['user_id']!=-1:
            customer_id = request.session['user_id']

            print_all_sql("SELECT CUSTOMER_ID,TYPE,DESCRIPTION,TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'HR'),TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'min')" +
                    "FROM SERVICE_REQUEST " +
                    "WHERE ORDER_ID IS NULL " +
                    "AND CUSTOMER_ID =" + str(customer_id) +
                    "ORDER BY TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'min')" +
                    " ;")


            for row in cursor.execute(
                    "SELECT CUSTOMER_ID,TYPE,DESCRIPTION,TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'HR'),TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'min')" +
                    "FROM SERVICE_REQUEST " +
                    "WHERE ORDER_ID IS NULL " +
                    "AND CUSTOMER_ID =" + str(customer_id) +
                    "ORDER BY TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'min')" +
                    " ;"):
                data_dict = {}
                data_dict['Type'] = row[1]
                data_dict['Description'] = row[2]
                request_time_hr = row[3]
                request_time_min = row[4]
                data_dict['Request_time'] = str(request_time_min) + " minute(s) ago"
                if float(request_time_hr)>=1 :
                    data_dict['Request_time'] = str(request_time_hr) + " hour(s) ago"
                else :
                    data_dict['Request_time'] = str(request_time_min) + " minute(s) ago"
                # print_all_sql(data_dict['Request_time'])
                pending_data.append(data_dict)

            print_all_sql("""
            SELECT o.ORDER_ID, sp.FIRST_NAME || ' ' || sp.LAST_NAME AS NAME, sp.TYPE, sp.PHONE_NUMBER
            FROM CUSTOMER c, SERVICE_REQUEST sr, ORDER_INFO o, SERVICE_PROVIDER sp
            WHERE c.CUSTOMER_ID = """+str(customer_id)+"""
            AND c.CUSTOMER_ID = sr.CUSTOMER_ID
            AND sr.ORDER_ID = o.ORDER_ID
            AND sp.WORKER_ID = o.TEAM_LEADER_ID
            AND o.TEAM_LEADER_ID = ANY( SELECT TEAM_LEADER_ID FROM GROUP_FORM WHERE CUSTOMER_APPROVED=0);""")



            for row in cursor.execute("""
            SELECT o.ORDER_ID, sp.FIRST_NAME || ' ' || sp.LAST_NAME AS NAME, sp.TYPE, sp.PHONE_NUMBER
            FROM CUSTOMER c, SERVICE_REQUEST sr, ORDER_INFO o, SERVICE_PROVIDER sp
            WHERE c.CUSTOMER_ID = """+str(customer_id)+"""
            AND c.CUSTOMER_ID = sr.CUSTOMER_ID
            AND sr.ORDER_ID = o.ORDER_ID
            AND sp.WORKER_ID = o.TEAM_LEADER_ID
            AND o.TEAM_LEADER_ID = ANY( SELECT TEAM_LEADER_ID FROM GROUP_FORM WHERE CUSTOMER_APPROVED=0);"""):
                data_dict = {}
                data_dict['order_id'] = row[0]
                data_dict['Team_leader_name'] = row[1]
                data_dict['Type'] = row[2]
                data_dict['worker_contact_no'] = row[3]

                payment = None
                for row2 in cursor.execute("""SELECT PAYMENT_PER_HOUR
                FROM SERVICE_PROVIDER
                GROUP BY PAYMENT_PER_HOUR,TYPE
                HAVING TYPE = '"""+data_dict['Type']+"""';""") :
                    payment = row2[0]
                data_dict['Estimated_payment'] = str(payment*3) + ' Tk./hr'

                group_data.append(data_dict)


            print_all_sql("""
                    SELECT S.CUSTOMER_ID, S.ORDER_ID,O.TYPE,O.START_TIME,O.END_TIME,ROUND((SELECT PAYMENT_PER_HOUR FROM SERVICE_PROVIDER WHERE WORKER_ID=O.WORKER_ID)*TIMEDIFF2(O.END_TIME,O.START_TIME,'sec')/3600,2) AS PAYMENT
                    FROM SERVICE_REQUEST S, ORDER_INFO O
                    WHERE S.ORDER_ID = O.ORDER_ID  
                    AND CHECK_GROUP_EXISTS_AND_APPROVED(O.ORDER_ID) = 1
                    AND S.CUSTOMER_ID = """+str(customer_id)+"""
                    ORDER BY O.START_TIME;""")

            for row in cursor.execute("""
                    SELECT S.CUSTOMER_ID, S.ORDER_ID,O.TYPE,O.START_TIME,O.END_TIME,ROUND((SELECT PAYMENT_PER_HOUR FROM SERVICE_PROVIDER WHERE WORKER_ID=O.WORKER_ID)*TIMEDIFF2(O.END_TIME,O.START_TIME,'sec')/3600,2) AS PAYMENT,O.TEAM_LEADER_ID
                    FROM SERVICE_REQUEST S, ORDER_INFO O
                    WHERE S.ORDER_ID = O.ORDER_ID  
                    AND CHECK_GROUP_EXISTS_AND_APPROVED(O.ORDER_ID) = 1
                    AND S.CUSTOMER_ID = """+str(customer_id)+"""
                    ORDER BY O.START_TIME;"""):
                data_dict = {}
                data_dict['Order_id'] = row[1]
                print(data_dict['Order_id'])
                data_dict['Type'] = row[2]
                start_time = row[3]
                end_time = row[4]
                if start_time != None :
                    start_time = start_time.strftime("%m/%d/%Y, %H:%M:%S")
                if end_time != None :
                    end_time = end_time.strftime("%m/%d/%Y, %H:%M:%S")
                data_dict['Start_time'] = start_time
                data_dict['End_time'] = end_time
                grp_has = row[6]
                if grp_has == None :
                    data_dict['Payment'] = row[5]
                else :
                    if row[5] != None :
                        data_dict['Payment'] = 3*row[5]
                    else :
                        data_dict['Payment'] = row[5]
                data.append(data_dict)

        if len(data) == 0 :
            empty = True
        if len(pending_data) == 0 :
            emptyPending = True
        if len(data) == 0 :
            empty = True
        if len(group_data) == 0 :
            emptyGrp = True

        ordertable = OrderTable(data)
        pendingtable = PendingTable(pending_data)
        grouptable = GroupTable(group_data)
        return render(request, 'home_customer/orders.html',{'title' : 'Orders','loggedIn' : request.session['loggedIn'],
                                                            'user_type' : request.session['user_type'],
                                                            'ordertable' : ordertable,'pendingtable' : pendingtable,
                                                            'grouptable' : grouptable,
                                                            'empty' : empty,'emptyPending' : emptyPending,
                                                            'emptyGrp' : emptyGrp})
    else :
        return redirect('home_customer-home')


def approveGroup(request,order_id) :

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

    #data_dict ={}

    connection.cursor().execute(""" UPDATE GROUP_FORM SET CUSTOMER_APPROVED = 1 WHERE ORDER_ID = """ + str(order_id) + """ ;""")


    return redirect('home_customer-orders')



def request_service(request,type) :
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-home')
        if 'user_id' in request.session and request.session['user_id'] != -1:
            customer_id = request.session['user_id']
            if request.method == 'POST':
                form = ServiceRequestForm(request.POST)
                if form.is_valid():
                    description = form.cleaned_data.get('description')
                    req_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for i in JOB_LIST:
                        if int(i[0]) == int(type):
                            type = i[1]
                            break
                    description = replaceNoneWithNull(description)
                    connection.cursor().execute(
                            "INSERT INTO SERVICE_REQUEST(CUSTOMER_ID,TYPE,DESCRIPTION,REQ_TIME)"
                            + " VALUES ('" + str(customer_id) + "','" + str(type) + "','" + str(description) + "'," + "TO_TIMESTAMP('" + str(req_time) + "','YYYY-MM-DD HH24:MI:SS')" + ");" )
                    print_all_sql("INSERT INTO SERVICE_REQUEST(CUSTOMER_ID,TYPE,DESCRIPTION,REQ_TIME)"
                            + " VALUES ('" + str(customer_id) + "','" + str(type) + "','" + str(description) + "'," + "TO_TIMESTAMP('" + str(req_time) + "','YYYY-MM-DD HH24:MI:SS')" + ");")

                    messages.success(request, "Your order was placed successfully.")
                    return redirect('home_customer-orders')

            else:
                form = ServiceRequestForm()
                for i in JOB_LIST:
                    if int(i[0]) == int(type):
                        type = i[1]
                        break
            return render(request, 'home_customer/request.html', {'title': 'Request','form': form,'type' : type})

    else:
        return redirect('home_customer-home')


def request_electrician(request) :
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-home')
        if 'user_id' in request.session and request.session['user_id'] != -1:
            customer_id = request.session['user_id']
            if request.method == 'POST':
                form = ElectricianRequestForm(request.POST)
                if form.is_valid():
                    type = form.cleaned_data.get('type')
                    description = form.cleaned_data.get('description')
                    req_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    description = replaceNoneWithNull(description)
                    connection.cursor().execute(
                            "INSERT INTO SERVICE_REQUEST(CUSTOMER_ID,TYPE,APPLIANCES_ID,DESCRIPTION,REQ_TIME)"
                            + " VALUES ('" + str(customer_id) + "','Electrician',"+ str(type) + ",'" + str(description) + "'," + "TO_TIMESTAMP('" + str(req_time) + "','YYYY-MM-DD HH24:MI:SS')" + ");" )

                    print_all_sql("INSERT INTO SERVICE_REQUEST(CUSTOMER_ID,TYPE,APPLIANCES_ID,DESCRIPTION,REQ_TIME)"
                            + " VALUES ('" + str(customer_id) + "','Electrician',"+ str(type) + ",'" + str(description) + "'," + "TO_TIMESTAMP('" + str(req_time) + "','YYYY-MM-DD HH24:MI:SS')" + ");")

                    messages.success(request, "Your order was placed successfully.")
                    return redirect('home_customer-orders')


            else:
                form = ElectricianRequestForm()
                type = "Electrician"
            return render(request, 'home_customer/request.html', {'title': 'Request','form': form,'type':type})

    else:
        return redirect('home_customer-home')


def rate(request, rating, Order_id) :
    # print_all_sql(rating,Order_id)
    if 'loggedIn' in request.session and request.session['loggedIn'] == True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            sql = """
            DECLARE
            ID NUMBER;
            BEGIN
                SELECT WORKER_ID INTO ID FROM ORDER_INFO WHERE ORDER_ID=""" + str(Order_id) + """;
                CALCRATING(""" + str(rating) + """,ID,'WORKER');
            END ;
            """
            print_all_sql(sql)
            connection.cursor().execute(sql)
            messages.success(request, "Thank you for your feedback.")
            return redirect('home_customer-orders')
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            sql = """
            DECLARE
            ID NUMBER;
            BEGIN
                SELECT CUSTOMER_ID INTO ID FROM SERVICE_REQUEST WHERE ORDER_ID=""" + str(Order_id) + """;
                CALCRATING(""" + str(rating) + """,ID,'CUSTOMER');
            END ;
            """
            print_all_sql(sql)
            connection.cursor().execute(sql)
            messages.success(request, "Thank you for your feedback.")
            return redirect('home_worker-orders')
    else:
        return redirect('login')