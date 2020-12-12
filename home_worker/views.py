from django.shortcuts import render,redirect
from django.db import connection
from customers.forms import *
# Create your views here.
from workers.views import replaceNoneWithNull
import django_tables2 as tables
from django_tables2 import TemplateColumn
import datetime
from django.contrib import messages
from home.views import *

cursor = connection.cursor()


def home(request):
    if 'loggedIn' in request.session and 'user_id' in request.session:
        first_name = ""
        if request.session['user_id'] != -1 : # if a user is logged in
            # print_all_sql(request.session['user_id'])
            if 'user_type' in request.session and request.session['user_type'] == "customer" :
                return redirect('home_customer-home')
            # TODO HOME-WORKER WELCOME
            print_all_sql("SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']))

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
        # TODO WORKER PROFILE
        print_all_sql("SELECT FIRST_NAME || ' ' || LAST_NAME,TYPE,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING,RATED_BY FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']))

        for row in cursor.execute(
                "SELECT FIRST_NAME || ' ' || LAST_NAME,TYPE,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING,RATED_BY FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id'])):
            name = row[0]
            type = row[1]
            phone_number = row[2]
            dob = row[3]
            thana = row[4]
            rating = row[5]
            rated_by = row[6]
            if rating==None or rated_by==None:
                rating = 0
                rated_by = 0



        return render(request, 'home_worker/about.html',{'title' : 'Profile','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],
                                                           'name' : name,'type' : type,'phone_number' : phone_number,
                                                           'dob' : dob,'thana' : thana,
                                                           'rating' : (float(rating)*100)/5,
                                                            'rated_by' : int(rated_by)})
    else :
        return redirect('home_customer-home')


class CurrentlyAvailableRequestsWithGroup(tables.Table):
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    customer_address =  tables.Column(verbose_name='Address')
    rating = tables.Column(verbose_name='Rating')
    description = tables.Column(verbose_name='Description')
    request_time = tables.Column(verbose_name='Request Time')
    accept_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequest"  record.req_no  %}">Accept</a>',verbose_name='Accept')
    accept_grp_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequestAndGroup"  record.req_no  %}">Accept and Ask for Group</a>',verbose_name='Ask for Group')

    class Meta:
        template_name = "django_tables2/bootstrap.html"

class CurrentlyAvailableRequests(tables.Table):
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    customer_address =  tables.Column(verbose_name='Address')
    rating = tables.Column(verbose_name='Rating')
    description = tables.Column(verbose_name='Description')
    request_time = tables.Column(verbose_name='Request Time')
    accept_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequest"  record.req_no  %}">Accept</a>',verbose_name='Accept')

    class Meta:
        template_name = "django_tables2/bootstrap.html"


class GroupRequests(tables.Table):
    worker_name = tables.Column(verbose_name='Requested By')
    customer_name = tables.Column(verbose_name='Customer Name')
    customer_phone_number = tables.Column(verbose_name='Phone Number')
    customer_address =  tables.Column(verbose_name='Address')
    description = tables.Column(verbose_name='Description')
    accept_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptGroupRequest"  record.order_id  %}">Accept</a>',verbose_name='Accept Group Request')

    class Meta:
        template_name = "django_tables2/bootstrap.html"



def orders(request):
    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        print_all_sql("SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']))

        for row in cursor.execute(
                "SELECT FIRST_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id'])):
            first_name = row[0]

        data = []
        group_data = []
        request_data = []
        emptyGRP = False
        cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if 'user_id' in request.session and request.session['user_id']!=-1:
            worker_id = request.session['user_id']

            sql = ""
            for row in connection.cursor().execute('SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID=' + str(worker_id) +';'):
                worker_type = row[0]

            print(worker_type)

            #TODO HOME-WORKER CURRENT AVAIALBLE JOB REQUESTS

            if worker_type == 'Electrician' :
                sql = """SELECT c.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,c.PHONE_NUMBER,c.ADDRESS,NVL(c.RATING,0),a.DESCRIPTION,a.REQ_TIME, TIMEDIFF2( SYSTIMESTAMP, a.REQ_TIME, 'HR'),TIMEDIFF2(SYSTIMESTAMP, a.REQ_TIME, 'min') , a.REQUEST_NO
                FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a
                WHERE c.THANA_NAME= s.THANA_NAME
                AND c.CUSTOMER_ID = ANY(SELECT a2.CUSTOMER_ID
                                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id)+""")
                AND a.CUSTOMER_ID = c.CUSTOMER_ID
                AND a.REQUEST_NO = ANY(SELECT a2.REQUEST_NO
                                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id)+""" AND a2.APPLIANCES_ID = ANY(SELECT APPLIANCES_ID FROM AREA_OF_EXPERTISE WHERE WORKER_ID="""+str(worker_id)+"""))
                AND s.WORKER_ID="""+str(worker_id)+""";"""
            else :
                sql = """             
            SELECT c.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,c.PHONE_NUMBER,c.ADDRESS,NVL(c.RATING,0),a.DESCRIPTION,a.REQ_TIME, TIMEDIFF2( SYSTIMESTAMP, a.REQ_TIME, 'HR'),TIMEDIFF2(SYSTIMESTAMP, a.REQ_TIME, 'min') , a.REQUEST_NO
            FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a
            WHERE c.THANA_NAME= s.THANA_NAME
            AND c.CUSTOMER_ID = ANY(SELECT a2.CUSTOMER_ID
                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id) +""")
            AND a.CUSTOMER_ID = c.CUSTOMER_ID
            AND a.REQUEST_NO = ANY(SELECT a2.REQUEST_NO
                        FROM SERVICE_REQUEST a2,SERVICE_PROVIDER s2
                        WHERE a2.Order_id IS NULL AND LOWER(a2.TYPE)= LOWER(s2.TYPE) AND s2.WORKER_ID="""+str(worker_id) +""")
            AND s.WORKER_ID="""+str(worker_id) +""";"""

            print_all_sql(sql)
            for row in cursor.execute(sql):
                data_dict = {}
                data_dict['customer_name'] = row[0]
                data_dict['customer_phone_number'] = row[1]
                data_dict['customer_address'] = row[2]
                data_dict['rating'] = float(row[3])
                data_dict['description'] = row[4]
                request_time_hr = row[6]
                request_time_min = row[7]

                data_dict['req_no'] = row[8]

                # print_all_sql("THIS IS BEFORE TABLE ", row[7])

                data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                if float(request_time_hr)>=1 :
                    data_dict['request_time'] = str(request_time_hr) + " hour(s) ago"
                else :
                    data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                data.append(data_dict)
            # TODO HOME-WORKER CURRENT AVAIALBLE JOB REQUESTS - CHECK GROUP ALLOWED
            group_is_allowed_for_this_user = connection.cursor().callfunc("CHECK_IF_GROUP_ALLOWED", bool, [worker_id])
            if group_is_allowed_for_this_user == True :
                availableRequestTable = CurrentlyAvailableRequestsWithGroup(data)
            else :
                availableRequestTable = CurrentlyAvailableRequests(data)
                emptyGRP = True
            empty = False
            if len(data) == 0 :
                empty = True

            # TODO HOME-WORKER GROUP FORMATION REQUESTS
            print_all_sql("""
            SELECT s.FIRST_NAME || ' ' || s.LAST_NAME AS NAME, c.FIRST_NAME || ' ' ||c.LAST_NAME AS CUSTOMER_NAME, c.PHONE_NUMBER, c.ADDRESS AS CUSTOMER_ADDRESS, a.DESCRIPTION, gf.ORDER_ID
            FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a, GROUP_FORM gf
            WHERE s.WORKER_ID = gf.TEAM_LEADER_ID
            AND c.CUSTOMER_ID = a.CUSTOMER_ID
            AND a.ORDER_ID = gf.ORDER_ID
            AND a.TYPE = (SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID = """+str(worker_id)+""")
            AND gf.GROUP_SIZE < 2 
            AND gf.TEAM_LEADER_ID != """+str(worker_id)+""" AND NVL(gf.WORKER_ID,0)!="""+str(worker_id)+""" AND NVL(gf.WORKER_ID_2,0) != """+str(worker_id)+""" AND s.THANA_NAME = (SELECT THANA_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID ="""+str(worker_id)+""");""")


            for row in cursor.execute("""
            SELECT s.FIRST_NAME || ' ' || s.LAST_NAME AS NAME, c.FIRST_NAME || ' ' ||c.LAST_NAME AS CUSTOMER_NAME, c.PHONE_NUMBER, c.ADDRESS AS CUSTOMER_ADDRESS, a.DESCRIPTION, gf.ORDER_ID
            FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a, GROUP_FORM gf
            WHERE s.WORKER_ID = gf.TEAM_LEADER_ID
            AND c.CUSTOMER_ID = a.CUSTOMER_ID
            AND a.ORDER_ID = gf.ORDER_ID
            AND a.TYPE = (SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID = """+str(worker_id)+""")
            AND gf.GROUP_SIZE < 2 
            AND gf.TEAM_LEADER_ID != """+str(worker_id)+""" AND NVL(gf.WORKER_ID,0)!="""+str(worker_id)+""" AND NVL(gf.WORKER_ID_2,0) != """+str(worker_id)+""" AND s.THANA_NAME = (SELECT THANA_NAME FROM SERVICE_PROVIDER WHERE WORKER_ID ="""+str(worker_id)+""");"""


):
                data_dict = {}
                data_dict['worker_name'] = row[0]
                data_dict['customer_name'] = row[1]
                data_dict['customer_phone_number'] = row[2]
                data_dict['customer_address'] = row[3]
                data_dict['description'] = row[4]
                data_dict['order_id'] = row[5]
                group_data.append(data_dict)
            groupRequestTable = GroupRequests(group_data)
            if len(group_data) == 0:
                emptyGRP = True

            return render(request, 'home_worker/home.html',{'title' : 'Home','loggedIn' : request.session['loggedIn'],'user_type' : request.session['user_type'],'first_name': first_name, 'empty' : empty, 'emptyGRP' : emptyGRP, 'availableRequestTable' : availableRequestTable, 'groupRequestTable' : groupRequestTable})
    else :
        return redirect('home_customer-home')


def acceptRequest(request, req_no):

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

        # TODO HOME-WORKER ACCEPT JOB REQUEST BUTTON
        print_all_sql("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID,REQUEST_NO)
                                VALUES( (SELECT TYPE
                                FROM SERVICE_PROVIDER
                                WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) +""",""" + str(req_no) +  """);"""
                            )


        connection.cursor().execute("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID,REQUEST_NO)
                                VALUES( (SELECT TYPE
                                FROM SERVICE_PROVIDER
                                WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) +""",""" + str(req_no) +  """);"""
                            )

        # TODO HOME-WORKER INSERT ORDER ID IN SERVICE REQUEST TABLE
        print_all_sql("""UPDATE SERVICE_REQUEST
                SET ORDER_ID = (SELECT ORDER_ID
                FROM ORDER_INFO
                WHERE REQUEST_NO = """ + str(req_no) +""")
                WHERE REQUEST_NO = """ + str(req_no) + """;""")


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

def acceptRequestAndGroup(request, req_no):

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

        # print_all_sql("Worker_ID = ", worker_id)

        # TODO HOME-WORKER ACCEPT AND ASK FOR GROUP BUTTON
        print_all_sql("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID,REQUEST_NO)
                                VALUES( (SELECT TYPE
                                FROM SERVICE_PROVIDER
                                WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) +""",""" + str(req_no) +  """);"""
                            )


        connection.cursor().execute("""INSERT INTO ORDER_INFO(TYPE, WORKER_ID,REQUEST_NO)
                                VALUES( (SELECT TYPE
                                FROM SERVICE_PROVIDER
                                WHERE WORKER_ID =""" + str(worker_id) + """),""" + str(worker_id) +""",""" + str(req_no) +  """);"""
                            )


        print_all_sql("""UPDATE SERVICE_REQUEST
                SET ORDER_ID = (SELECT ORDER_ID
                FROM ORDER_INFO
                WHERE REQUEST_NO = """ + str(req_no) +""")
                WHERE REQUEST_NO = """ + str(req_no) + """;""")


        connection.cursor().execute(
            """UPDATE SERVICE_REQUEST
                SET ORDER_ID = (SELECT ORDER_ID
                FROM ORDER_INFO
                WHERE REQUEST_NO = """ + str(req_no) +""")
                WHERE REQUEST_NO = """ + str(req_no) + """;"""
        )

        # TODO HOME-WORKER CREATE GROUP REQUEST PROCEDURE

        connection.cursor().execute(""" 
        BEGIN
	        CREATE_GROUP_REQUEST(""" + str(req_no) +""", """ + str(worker_id) + """ );
        END;
        """)

        # insert the order id,team leader id into group form
        connection.cursor().execute(""" INSERT INTO GROUP_FORM(ORDER_ID, GROUP_SIZE, TEAM_LEADER_ID)
        VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO = """ + str(req_no) + """ ), 0, """ + str(worker_id) + """);""")

        print_all_sql(""" INSERT INTO GROUP_FORM(ORDER_ID, GROUP_SIZE, TEAM_LEADER_ID)
        VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO = """ + str(req_no) + """ ), 0, """ + str(worker_id) + """);""")



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
    Order_id = tables.Column(verbose_name='Order ID')
    customer_name = tables.Column(verbose_name='Name')
    customer_phone = tables.Column(verbose_name='Phone Number')
    customer_address = tables.Column(verbose_name='Address')
    Start_time = tables.Column(verbose_name='Start Time')
    End_time = tables.Column(verbose_name='End Time')
    Payment = tables.Column(verbose_name='Payment Tk.')
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

            # TODO WORKER JOB HISTORY
            print_all_sql("""
                SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME,ROUND((s.PAYMENT_PER_HOUR*TIMEDIFF2(O.END_TIME,O.START_TIME,'sec'))/3600,2)
                FROM CUSTOMER C,ORDER_INFO O,SERVICE_PROVIDER S
                WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                FROM SERVICE_REQUEST SR
                                WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                AND O.START_TIME IS NOT NULL AND O.END_TIME IS NOT NULL AND O.ORDER_ID IS NOT NULL
                AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+""")
                AND S.WORKER_ID = """+str(worker_id)+""";""")


            for row in connection.cursor().execute("""
                SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME,ROUND((s.PAYMENT_PER_HOUR*TIMEDIFF2(O.END_TIME,O.START_TIME,'sec'))/3600,2)
                FROM CUSTOMER C,ORDER_INFO O,SERVICE_PROVIDER S
                WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                FROM SERVICE_REQUEST SR
                                WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                AND O.START_TIME IS NOT NULL AND O.END_TIME IS NOT NULL AND O.ORDER_ID IS NOT NULL
                AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+""")
                AND S.WORKER_ID = """+str(worker_id)+""";""") :

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


                data_dict['Payment'] = row[6]
                jobHistory.append(data_dict)

            # TODO WORKER JOB HISTORY IF WORKED IN GROUP

            print_all_sql("""
            SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,OI.ORDER_ID,OI.START_TIME,OI.END_TIME,ROUND((s.PAYMENT_PER_HOUR*TIMEDIFF2(OI.END_TIME,OI.START_TIME,'sec'))/3600,2)
            FROM GROUP_FORM GF,ORDER_INFO OI,CUSTOMER C, SERVICE_REQUEST SR,SERVICE_PROVIDER S
            WHERE OI.ORDER_ID = GF.ORDER_ID
            AND SR.ORDER_ID=OI.ORDER_ID
            AND C.CUSTOMER_ID=SR.CUSTOMER_ID
            AND OI.TEAM_LEADER_ID = GF.TEAM_LEADER_ID
            AND (GF.WORKER_ID = """+str(worker_id)+""" OR GF.WORKER_ID_2="""+str(worker_id)+""")
            AND S.WORKER_ID = """+str(worker_id)+"""
            AND OI.START_TIME IS NOT NULL AND OI.END_TIME IS NOT NULL
            ;""")
            for row in connection.cursor().execute("""
            SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,OI.ORDER_ID,OI.START_TIME,OI.END_TIME,ROUND((s.PAYMENT_PER_HOUR*TIMEDIFF2(OI.END_TIME,OI.START_TIME,'sec'))/3600,2)
            FROM GROUP_FORM GF,ORDER_INFO OI,CUSTOMER C, SERVICE_REQUEST SR,SERVICE_PROVIDER S
            WHERE OI.ORDER_ID = GF.ORDER_ID
            AND SR.ORDER_ID=OI.ORDER_ID
            AND C.CUSTOMER_ID=SR.CUSTOMER_ID
            AND OI.TEAM_LEADER_ID = GF.TEAM_LEADER_ID
            AND (GF.WORKER_ID = """+str(worker_id)+""" OR GF.WORKER_ID_2="""+str(worker_id)+""")
            AND S.WORKER_ID = """+str(worker_id)+"""
            AND OI.START_TIME IS NOT NULL AND OI.END_TIME IS NOT NULL
            ;"""):

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

                data_dict['Payment'] = row[6]
                jobHistory.append(data_dict)



            # TODO WORKER CURRENTLY RUNNING JOBS
            print_all_sql("""SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                            FROM CUSTOMER C,ORDER_INFO O
                            WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                                                        FROM SERVICE_REQUEST SR
                                                                        WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                            AND O.ORDER_ID IS NOT NULL AND O.END_TIME IS NULL
                            AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+""")
                            AND CHECK_GROUP_EXISTS_AND_APPROVED(O.ORDER_ID)=1;""")


            for row in connection.cursor().execute(
                    """SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                            FROM CUSTOMER C,ORDER_INFO O
                            WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                                                        FROM SERVICE_REQUEST SR
                                                                        WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                            AND O.ORDER_ID IS NOT NULL AND O.END_TIME IS NULL
                            AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+""")
                            AND CHECK_GROUP_EXISTS_AND_APPROVED(O.ORDER_ID)=1;"""):

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
        # TODO WORKER START TIME BUTTON

        print_all_sql("""
        UPDATE ORDER_INFO
        SET START_TIME = SYSTIMESTAMP
        WHERE ORDER_ID = """+ str(order_id) +""";""")

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
        # TODO WORKER END TIME BUTTON
        print_all_sql("""
        UPDATE ORDER_INFO
        SET END_TIME = SYSTIMESTAMP
        WHERE ORDER_ID = """+ str(order_id) +""";""")


        connection.cursor().execute("""
        UPDATE ORDER_INFO
        SET END_TIME = SYSTIMESTAMP
        WHERE ORDER_ID = """+ str(order_id) +""";""")
        return redirect('home_worker-orders')
    else:
        return redirect('login')

def acceptGroupRequest(request,order_id) :

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

    # TODO WORKER ACCEPT GROUP REQUEST BUTTON
    connection.cursor().execute("""
    BEGIN
        ACCEPTING_GROUP_REQUEST(""" + str(order_id) + """,""" + str(worker_id) + """);
    END;
    """)


    return redirect('home_worker-orders')