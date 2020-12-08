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

        print_all_sql("SELECT FIRST_NAME || ' ' || LAST_NAME,TYPE,PHONE_NUMBER,TO_CHAR(DATE_OF_BIRTH,'DL'),THANA_NAME,RATING FROM SERVICE_PROVIDER WHERE WORKER_ID = " + str(request.session['user_id']))

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
    accept_grp_button = TemplateColumn('<a class="btn btn-dark" href="{% url "acceptRequestAndGroup"  record.req_no  %}">Accept and Ask for Group</a>',verbose_name='Ask for Group')

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
        cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if 'user_id' in request.session and request.session['user_id']!=-1:
            worker_id = request.session['user_id']


            print_all_sql("""             
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
            AND s.WORKER_ID="""+str(worker_id) +""";""")





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

                # print_all_sql("THIS IS BEFORE TABLE ", row[7])

                data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                if float(request_time_hr)>=1 :
                    data_dict['request_time'] = str(request_time_hr) + " hour(s) ago"
                else :
                    data_dict['request_time'] = str(request_time_min) + " minute(s) ago"
                data.append(data_dict)
            availableRequestTable = CurrentlyAvailableRequests(data)
            empty = False
            if len(data) == 0 :
                empty = True

            # TODO FARDIN (DONE) : ADD SQL BELOW TO MAKE GROUP REQUEST TABLE IN WORKER HOME
            # REMEMBER TO SELECT WORKER_NAME WHO REQUESTED GROUP, CUSTOMER_NAME, customer_phone_number, customer_address
            # description,ORDER_ID IN THAT ORDER
            # UNCOMMENT LINE 161-170

            sql = """"""
            print_all_sql("""
            SELECT s.FIRST_NAME || ' ' || s.LAST_NAME AS NAME, c.FIRST_NAME || ' ' ||c.LAST_NAME AS CUSTOMER_NAME, c.PHONE_NUMBER c.ADDRESS AS CUSTOMER_ADDRESS, a.DESCRIPTION, gf.ORDER_ID
            FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a, GROUP_FORM gf
            WHERE s.WORKER_ID = gf.TEAM_LEADER_ID
            AND c.CUSTOMER_ID = a.CUSTOMER_ID
            AND a.ORDER_ID = gf.ORDER_ID
            AND (SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID = """ + str(worker_id) +
            """) = ANY( SELECT TYPE FROM GROUP_FORM g, SERVICE_PROVIDER sp WHERE g.TEAM_LEADER_ID = sp.WORKER_ID); """)


            for row in cursor.execute("""
            SELECT s.FIRST_NAME || ' ' || s.LAST_NAME AS NAME, c.FIRST_NAME || ' ' ||c.LAST_NAME AS CUSTOMER_NAME, c.PHONE_NUMBER, c.ADDRESS AS CUSTOMER_ADDRESS, a.DESCRIPTION, gf.ORDER_ID
            FROM CUSTOMER c, SERVICE_PROVIDER s,SERVICE_REQUEST a, GROUP_FORM gf
            WHERE s.WORKER_ID = gf.TEAM_LEADER_ID
            AND c.CUSTOMER_ID = a.CUSTOMER_ID
            AND a.ORDER_ID = gf.ORDER_ID
            AND (SELECT sp1.TYPE FROM SERVICE_PROVIDER sp1 WHERE sp1.WORKER_ID = """ + str(worker_id) +
            """) = ANY( SELECT sp.TYPE FROM GROUP_FORM g, SERVICE_PROVIDER sp WHERE g.TEAM_LEADER_ID = sp.WORKER_ID)
            AND gf.GROUP_SIZE < 2 
            AND gf.TEAM_LEADER_ID != """ + str(worker_id) +
            """ AND s.THANA_NAME = ANY(SELECT s2.THANA_NAME FROM SERVICE_PROVIDER s2, GROUP_FORM g1 WHERE g1.TEAM_LEADER_ID = s2.WORKER_ID);"""):
                data_dict = {}
                data_dict['worker_name'] = row[0]
                data_dict['customer_name'] = row[1]
                data_dict['customer_phone_number'] = row[2]
                data_dict['customer_address'] = row[3]
                data_dict['description'] = row[4]
                data_dict['order_id'] = row[5]
                group_data.append(data_dict)
            groupRequestTable = GroupRequests(group_data)
            emptyGRP = False
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

        # TODO FARDIN : QUERY USING REQ_NO AND RETRIEVE ORDER_ID
        #  1. accept and ask for grp--> i.Team Leader id  and order_id inserted in grpE/grpP/grpH
        #                             ii. Team Leader id and order id inserted in group form table
        #                             WHEN GROUP SIZE==2 :
        #                                             Iii. INSERT TEAM_LEADER_ID IN ORDER INFO TABLE
        #                             (USE TRIGGER FOR THIS)

        data_dict_for_spType={}

        connection.cursor().execute(""" 
        BEGIN
	        CREATE_GROUP_REQUEST(""" + str(req_no) +""", """ + str(worker_id) + """ );
        END;
        """)

        # for row in cursor.execute(""" SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID =""" + str(worker_id) + """;"""):
        #     data_dict_for_spType['Service_provider_type'] = row[0]
        #
        #
        # print_all_sql(""" SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID =""" + str(worker_id) + """;""")
        # #type = row[0]
        #
        # #if type
        #
        # print("The service provider type is ", data_dict_for_spType)
        #
        # if(data_dict_for_spType['Service_provider_type'] == 'Pest Control Service'):
        #     connection.cursor().execute(""" INSERT INTO GROUP_PEST_CONTROL(ORDER_ID, TEAMLEADER_ID)
        #     VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(worker_id) + """);"""
        #     )
        #
        #     print_all_sql(""" INSERT INTO GROUP_PEST_CONTROL(ORDER_ID, TEAMLEADER_ID)
        #     VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(worker_id) + """);""")
        #
        # if (data_dict_for_spType['Service_provider_type'] == 'House Shifting Assistant'):
        #     connection.cursor().execute(""" INSERT INTO GROUP_HOUSE_SHIFTING_ASSISTANT(ORDER_ID, TEAMLEADER_ID)
        #             VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(
        #         worker_id) + """);""")
        #
        #     print_all_sql(""" INSERT INTO GROUP_HOUSE_SHIFTING_ASSISTANT(ORDER_ID, TEAMLEADER_ID)
        #             VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(
        #         worker_id) + """);""")
        #
        #
        # if (data_dict_for_spType['Service_provider_type'] == 'Electrician'):
        #     connection.cursor().execute(""" INSERT INTO GROUP_ELECTRICIAN(ORDER_ID, TEAMLEADER_ID)
        #             VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(
        #         worker_id) + """);""")
        #
        #     print_all_sql(""" INSERT INTO GROUP_ELECTRICIAN(ORDER_ID, TEAMLEADER_ID)
        #             VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO =""" + str(req_no) + """), """ + str(
        #         worker_id) + """);""")


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


            print_all_sql("""
                SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                FROM CUSTOMER C,ORDER_INFO O
                WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
												FROM SERVICE_REQUEST SR
												WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+str(worker_id)+"""))
                AND O.START_TIME IS NOT NULL AND O.END_TIME IS NOT NULL AND O.ORDER_ID IS NOT NULL
                AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID="""+ str(worker_id) +""")

												;""")


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



            #TODO FARDIN : MODIFY QUERY ( Currently running jobs er Query te add this →
            # First check korte hobe oi job tay group ase kina :
            # Order_id use kore group form e check korbe
            # team leader id null kina. Jodi group size==2 hoy and group form.team leader id jodi null na hoy,
            # tarmane group ase
            # Erpor Check korte hobe group ta customer approve korse kina :
            # order info table e team leader id ta null hoy that means oita customer approve korse.)

            print_all_sql("""
                        SELECT C.FIRST_NAME || ' ' || C.LAST_NAME AS NAME,C.PHONE_NUMBER,C.ADDRESS,O.ORDER_ID,O.START_TIME,O.END_TIME
                        FROM CUSTOMER C,ORDER_INFO O
                        WHERE C.CUSTOMER_ID = ANY(SELECT SR.CUSTOMER_ID
                                                        FROM SERVICE_REQUEST SR
                                                        WHERE SR.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID=""" + str(
                            worker_id) + """))
                            AND O.ORDER_ID IS NOT NULL AND O.END_TIME IS NULL
                            AND O.REQUEST_NO = ANY(SELECT O.REQUEST_NO FROM ORDER_INFO O WHERE O.WORKER_ID=""" + str(
                            worker_id) + """)

            												;""")


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
        # print_all_sql(jobHistory)
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

    #TODO FARDIN :  ADD SQL (loggedin worker id corresponding order id te grpPEH e insert hobe.
    # And trigger use kore group form table e automatically oi order id te group size increase 1,
    # jodi group size 2 hoye jay tahole INSERT TEAM_LEADER_ID IN ORDER INFO TABLE)

    if 'loggedIn' in request.session and request.session['loggedIn']==True:
        if 'user_type' in request.session and request.session['user_type'] == "customer":
            return redirect('home_customer-home')

        if 'user_id' in request.session and request.session['user_id'] != -1:
            worker_id = request.session['user_id']

    #print_all_sql()

    #connection.cursor().execute()

    data_dict_for_spType = {}

    data_dict={}

    for row in cursor.execute(""" SELECT TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID =""" + str(worker_id) + """;"""):
        data_dict_for_spType['Service_provider_type'] = row[0]

    if (data_dict_for_spType['Service_provider_type'] == 'Pest Control Service'):
        connection.cursor().execute(""" UPDATE GROUP_PEST_CONTROL 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;"""
                                    )

        print_all_sql(""" UPDATE GROUP_PEST_CONTROL 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")

    if (data_dict_for_spType['Service_provider_type'] == 'House Shifting Assistant'):
        connection.cursor().execute(""" UPDATE GROUP_HOUSE_SHIFTING_ASSISTANT 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")

        print_all_sql(""" UPDATE GROUP_HOUSE_SHIFTING_ASSISTANT 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")

    if (data_dict_for_spType['Service_provider_type'] == 'Electrician'):
        connection.cursor().execute(""" UPDATE GROUP_ELECTRICIAN 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")

        print_all_sql(""" UPDATE GROUP_ELECTRICIAN 
                                        SET WORKER_ID = """ + str(worker_id) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")

    connection.cursor().execute(""" UPDATE GROUP_FORM
                                    SET GROUP_SIZE = GROUP_SIZE + 1
                                    WHERE ORDER_ID = """ + str(order_id) + """;""")


    for row in cursor.execute(""" SELECT GROUP_SIZE FROM GROUP_FORM WHERE ORDER_ID =""" + str(order_id) + """;"""):
        data_dict['Group_size'] = row[0]

    if (data_dict['Group_size']==2):
        for row in cursor.execute(""" SELECT TEAM_LEADER_ID FROM GROUP_FORM WHERE ORDER_ID =""" + str(order_id) + """;"""):
            data_dict['Team_leader_id'] = row[0]

        connection.cursor().execute(""" UPDATE ORDER_INFO SET TEAM_LEADER_ID = """ + str(data_dict['Team_leader_id']) +
                                    """ WHERE ORDER_ID = """ + str(order_id) + """;""")


    return redirect('home_worker-orders')