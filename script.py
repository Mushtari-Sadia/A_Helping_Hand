import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_Helping_Hand.settings')
django.setup()


# with open('F:\L2-T2\CSE 216\Project\A_Helping_Hand\DDL.txt','r') as file:
#     ddl = file.read()
#
# print(ddl)
# connection.cursor().execute(str(ddl))


connection.cursor().execute("CREATE TABLE Customer(" +
                            "customer_id NUMBER GENERATED BY DEFAULT AS IDENTITY," +
                            "first_name VARCHAR2(50) NOT NULL," +
                            "last_name VARCHAR2(50) NOT NULL," + "password  VARCHAR2(40)  NOT NULL,"
                            + "phone_number VARCHAR2(11)," +
                            "thana_name VARCHAR2(30) NOT NULL," +
                            "address VARCHAR2(70)," +
                            "date_of_birth DATE NOT NULL," +
                            "rating NUMBER(2,1) CONSTRAINT RATING_CHK CHECK (rating BETWEEN 0.0 AND 5.0)," +
                            "CONSTRAINT CUSTOMER_PK PRIMARY KEY(customer_id) );"
                            )

connection.cursor().execute("CREATE TABLE Service_Provider(" +
                            "worker_id NUMBER GENERATED BY DEFAULT AS IDENTITY," +
                            "type VARCHAR2(30) NOT NULL," +
                            "first_name VARCHAR2(50) NOT NULL," +
                            "last_name VARCHAR2(50) NOT NULL," +
                            "password  VARCHAR2(40)  NOT NULL," +
                            "phone_number VARCHAR2(11)," +
                            "thana_name VARCHAR2(30) NOT NULL," +
                            "address VARCHAR2(70)," +
                            "date_of_birth DATE NOT NULL," +
                            "payment_per_hour NUMBER," +
                            "rating NUMBER(2,1) CONSTRAINT RATING_CHK2 CHECK (rating BETWEEN 0.0 AND 5.0)," +
                            "CONSTRAINT WORKER_PK PRIMARY KEY(worker_id));"
                            )



connection.cursor().execute("CREATE TABLE Order_Info( " +
                            "order_id NUMBER GENERATED BY DEFAULT AS IDENTITY," +
                            "type VARCHAR2(30) NOT NULL," +
                            "worker_id NUMBER," +
                            "start_time TIMESTAMP(0)," +
                            "end_time TIMESTAMP(0)," +
                            "CONSTRAINT ORDER_INFO_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
                            "CONSTRAINT ORDER_INFO_PK PRIMARY KEY(order_id)" + ");"
                            )



connection.cursor().execute("CREATE TABLE Emergency_Phone_Number(" +
                            "emergency_id NUMBER GENERATED BY DEFAULT AS IDENTITY," +
                            "emergency_type VARCHAR2(20) NOT NULL," +
                            "phone_number VARCHAR2(11) NOT NULL," +
                            "CONSTRAINT EMERGENCY_PK PRIMARY KEY(emergency_id));"
                            )


connection.cursor().execute("CREATE TABLE Electrician(" +
                            "worker_id NUMBER," +
                            "license_info VARCHAR2(20)," +
                            "years_of_experience NUMBER," +
                            "qualification VARCHAR2(50)," +
                            "CONSTRAINT ELECTRICIAN_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
                            "CONSTRAINT ELECTRICIAN_PK PRIMARY KEY(worker_id));"
                            )


connection.cursor().execute("CREATE TABLE Appliances("+
                            "appliances_id NUMBER GENERATED BY DEFAULT AS IDENTITY," +
                            "type VARCHAR2(20)," +
                            "CONSTRAINT APP_PK PRIMARY KEY(appliances_id));"
                            )

connection.cursor().execute("CREATE TABLE Home_Cleaner("+
                            "worker_id NUMBER," +
                            "NID NUMBER," +
                            "CONSTRAINT HOMECLEANER_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
                            "CONSTRAINT HOMECLEANER_PK PRIMARY KEY(worker_id));"
                            )


connection.cursor().execute("CREATE TABLE Pest_Control(" +
"worker_id NUMBER," +
"license_info VARCHAR2(20)," +
"chemical_info VARCHAR2(50)," +
"CONSTRAINT PEST_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
"CONSTRAINT PEST_PK PRIMARY KEY(worker_id));")


connection.cursor().execute("CREATE TABLE Plumber(" +
"worker_id NUMBER," +
"years_of_experience NUMBER," +
"CONSTRAINT PLUMBER_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
"CONSTRAINT PLUMBER_PK PRIMARY KEY(worker_id));")


connection.cursor().execute("CREATE TABLE Nurse(" +
"worker_id NUMBER," +
"certificate_info VARCHAR2(20)," +
"qualification VARCHAR2(50)," +
"years_of_experience NUMBER," +
"CONSTRAINT NURSE_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
"CONSTRAINT NURSE_PK PRIMARY KEY(worker_id));")


connection.cursor().execute("CREATE TABLE House_Shifting_Assistant("+
"worker_id NUMBER," +
"driving_license VARCHAR2(20)," +
"car_type VARCHAR2(20)," +
"car_no VARCHAR2(20)," +
"CONSTRAINT HOUSESA_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
"CONSTRAINT HOUSESA_PK PRIMARY KEY(worker_id));")


connection.cursor().execute("CREATE TABLE Carpenter("+
"worker_id NUMBER," +
"shop_name VARCHAR2(20)," +
"shop_address VARCHAR2(70)," +
"CONSTRAINT CARPENTER_FK FOREIGN KEY(worker_id) REFERENCES Service_Provider(worker_id) ON DELETE CASCADE," +
"CONSTRAINT CARPENTER_PK PRIMARY KEY(worker_id));")


connection.cursor().execute("CREATE TABLE Service_Request("+
            "Request_no NUMBER GENERATED BY DEFAULT AS IDENTITY," +
            "customer_id NUMBER," +
            "order_id NUMBER," +
            "type VARCHAR2(30) NOT NULL," +
            "description VARCHAR2(60)," +
            "appliances_id NUMBER," +
            "req_time TIMESTAMP(0) NOT NULL," +
            "CONSTRAINT SERVICE_REQUEST_FK1 FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)," +
            "CONSTRAINT SERVICE_REQUEST_FK2 FOREIGN KEY(order_id) REFERENCES Order_Info(order_id)," +
            "CONSTRAINT SERVICE_REQUEST_FK3 FOREIGN KEY(appliances_id) REFERENCES Appliances(appliances_id)," +
            "CONSTRAINT SERVICE_REQUEST_PK PRIMARY KEY(Request_no));")


connection.cursor().execute("CREATE TABLE In_An_Emergency("+
"emergency_id NUMBER," +
"customer_id NUMBER," +
"CONSTRAINT In_An_Emergency_FK1 FOREIGN KEY (emergency_id) REFERENCES Emergency_Phone_Number(emergency_id)," +
"CONSTRAINT In_An_Emergency_FK2 FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)," +
"CONSTRAINT In_An_Emergency_PK PRIMARY KEY(emergency_id,customer_id));")

connection.cursor().execute("CREATE TABLE Area_Of_Expertise("+
"worker_id NUMBER," +
"appliances_id NUMBER," +
"CONSTRAINT AREA_OF_EXPERTISE_FK1 FOREIGN KEY(worker_id) REFERENCES Electrician(worker_id)," +
"CONSTRAINT AREA_OF_EXPERTISE_FK2 FOREIGN KEY(appliances_id) REFERENCES Appliances(appliances_id)," +
                            "CONSTRAINT AREA_OF_EXPERTISE_PK PRIMARY KEY(worker_id,appliances_id));")


connection.cursor().execute("CREATE TABLE Group_Electrician("+
"order_id NUMBER," +
"worker_id NUMBER," +
"teamLeader_id NUMBER," +
"CONSTRAINT GROUP_ELECTRICIAN_FK1 FOREIGN KEY(order_id) REFERENCES Order_Info(order_id)," +
"CONSTRAINT GROUP_ELECTRICIAN_FK2 FOREIGN KEY(worker_id) REFERENCES Electrician(worker_id)," +
"CONSTRAINT GROUP_ELECTRICIAN_PK PRIMARY KEY(order_id));")

connection.cursor().execute("CREATE TABLE Group_Pest_Control("+
"order_id NUMBER," +
"worker_id NUMBER," +
"teamLeader_id NUMBER," +
"CONSTRAINT GROUP_PEST_FK1 FOREIGN KEY(order_id) REFERENCES Order_Info(order_id)," +
"CONSTRAINT GROUP_PEST_FK2 FOREIGN KEY(worker_id) REFERENCES Pest_Control(worker_id)," +
"CONSTRAINT GROUP_PEST_PK PRIMARY KEY(order_id));")


connection.cursor().execute("CREATE TABLE Group_House_Shifting_Assistant("+
"order_id NUMBER," +
"worker_id NUMBER," +
"teamLeader_id NUMBER," +
"CONSTRAINT GROUP_HOUSE_FK1 FOREIGN KEY(order_id) REFERENCES Order_Info(order_id)," +
"CONSTRAINT GROUP_HOUSE_FK2 FOREIGN KEY(worker_id) REFERENCES House_Shifting_Assistant (worker_id)," +
"CONSTRAINT GROUP_HOUSE_PK PRIMARY KEY(order_id));")





OPTIONS = [
        (1, "AC"),
        (2, "TV"),
        (3, "FRIDGE"),
        (4, "GENERAL"),
    ]

for i in OPTIONS:
	connection.cursor().execute("INSERT INTO APPLIANCES(APPLIANCES_ID,TYPE)" + " VALUES ('" + str(i[0]) + "','"  + str(i[1]) + "')")