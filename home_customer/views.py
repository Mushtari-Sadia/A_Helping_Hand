from django.shortcuts import render,redirect
from django.db import connection
from customers.forms import JOB_LIST
import django_tables2 as tables
# Create your views here.
cursor = connection.cursor()

def home(request):
    if 'loggedIn' in request.session and 'user_id' in request.session:
        first_name = ""
        if request.session['user_id'] != -1 : # if a user is logged in
            print(request.session['user_id'])
            if 'user_type' in request.session and request.session['user_type'] == "worker" :
                return redirect('home_worker-home')
            for row in cursor.execute("SELECT FIRST_NAME FROM CUSTOMER WHERE CUSTOMER_ID = " + str(request.session['user_id']) ):
                first_name = row[0]
            return render(request, 'home_customer/home.html',{'loggedIn' : request.session['loggedIn'], 'first_name' : first_name})
        else :
            return redirect('login')
    return redirect('login')

def about(request):
    if 'loggedIn' in request.session:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-about')
        return render(request, 'home_customer/about.html',{'title' : 'About','loggedIn' : request.session['loggedIn']})
    else :
        return render(request, 'home_customer/about.html', {'title': 'About'})


class OrderTable(tables.Table):
    Order_id = tables.Column(verbose_name='Order ID')
    Type = tables.Column(verbose_name='Service Provider')
    Start_time = tables.Column(verbose_name='Start Time')
    End_time = tables.Column(verbose_name='End Time')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class PendingTable(tables.Table):
    Type = tables.Column(verbose_name='Service Provider')
    Description = tables.Column(verbose_name='Description')

    class Meta:
        template_name = "django_tables2/bootstrap.html"



def orders(request):
    if 'loggedIn' in request.session:
        if 'user_type' in request.session and request.session['user_type'] == "worker":
            return redirect('home_worker-home')

        data = []
        pending_data = []
        if 'user_id' in request.session and request.session['user_id']!=-1:
            customer_id = request.session['user_id']

            for row in cursor.execute(
                    "SELECT CUSTOMER_ID,TYPE,DESCRIPTION " +
                    "FROM SERVICE_REQUEST " +
                    "WHERE ORDER_ID IS NULL " +
                    "AND CUSTOMER_ID =" + str(customer_id) + " ;"):
                data_dict = {}
                data_dict['Type'] = row[1]
                data_dict['Description'] = row[2]
                pending_data.append(data_dict)

            for row in cursor.execute(
                    "SELECT S.CUSTOMER_ID, S.ORDER_ID, O.ORDER_ID,O.TYPE,O.START_TIME,O.END_TIME " +
                    "FROM SERVICE_REQUEST S, ORDER_INFO O " +
                    "WHERE S.ORDER_ID = O.ORDER_ID " +
                    "AND S.CUSTOMER_ID =" + str(customer_id) + " ORDER BY O.START_TIME;")  :
                data_dict = {}
                data_dict['Order_id'] = row[2]
                data_dict['Type'] = row[3]
                data_dict['Start_time'] = row[4].strftime("%m/%d/%Y, %H:%M:%S")
                data_dict['End_time'] = row[5].strftime("%m/%d/%Y, %H:%M:%S")
                data.append(data_dict)


        ordertable = OrderTable(data)
        pendingtable = PendingTable(pending_data)
        return render(request, 'home_customer/orders.html',{'title' : 'Orders','loggedIn' : request.session['loggedIn'],'ordertable' : ordertable,'pendingtable' : pendingtable})
    else :
        return render(request, 'home_customer/homw.html', {'title': 'Home'})
