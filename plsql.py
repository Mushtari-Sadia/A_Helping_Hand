import os
import django
from django.db import connection
from home.views import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_Helping_Hand.settings')
django.setup()

#TODO FUNCTION TIMEDIFF
timediff = """
    CREATE OR REPLACE FUNCTION TIMEDIFF2(TIME1 IN TIMESTAMP,TIME2 IN TIMESTAMP,UNIT IN VARCHAR2)
    RETURN NUMBER IS
            TD INTERVAL DAY TO SECOND := TIME1 - TIME2;
            TS NUMBER;

    BEGIN

            TS := EXTRACT(DAY FROM TD)*86400;
            TS := TS + EXTRACT(HOUR FROM TD)*3600;
            TS := TS + EXTRACT(MINUTE FROM TD)*60;
            TS := TS + EXTRACT(SECOND FROM TD);

            IF LOWER(UNIT)='sec' THEN
                TS:= TS/1;
            ELSIF LOWER(UNIT)='min' THEN
                TS:= TS/60;
            ELSIF LOWER(UNIT)='hr' THEN
                TS:=TS/3600;
            ELSIF LOWER(UNIT)='day' THEN
                TS:=TS/86400;
            END IF;

            RETURN ROUND(TS,0);

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
                RETURN NULL;
        WHEN OTHERS THEN
                RETURN NULL;


    END;
"""
#TODO PROCEDURE CALCRATING

calcrating = """
CREATE OR REPLACE PROCEDURE CALCRATING(NEW_RATING IN NUMBER,ID IN NUMBER,USER IN VARCHAR2) IS
		OVERALL_RATING NUMBER;
		TOTAL_RATING NUMBER;

BEGIN

		IF LOWER(USER)='customer' THEN
				SELECT NVL(RATING,0),NVL(RATED_BY,0) INTO OVERALL_RATING,TOTAL_RATING FROM CUSTOMER WHERE CUSTOMER_ID=ID;

				OVERALL_RATING := ((OVERALL_RATING * TOTAL_RATING) + NEW_RATING) / (TOTAL_RATING + 1);
				OVERALL_RATING := ROUND(OVERALL_RATING,1);
				TOTAL_RATING := TOTAL_RATING + 1;

				UPDATE CUSTOMER SET RATING=OVERALL_RATING WHERE CUSTOMER_ID=ID;
				UPDATE CUSTOMER SET RATED_BY=TOTAL_RATING WHERE CUSTOMER_ID=ID;

		ELSIF LOWER(USER)='worker' THEN
				SELECT NVL(RATING,0),NVL(RATED_BY,0) INTO OVERALL_RATING,TOTAL_RATING FROM SERVICE_PROVIDER WHERE WORKER_ID=ID;

				OVERALL_RATING := ((OVERALL_RATING * TOTAL_RATING) + NEW_RATING) / (TOTAL_RATING + 1);
				TOTAL_RATING := TOTAL_RATING + 1;

				UPDATE SERVICE_PROVIDER SET RATING=OVERALL_RATING WHERE WORKER_ID=ID;
				UPDATE SERVICE_PROVIDER SET RATED_BY=TOTAL_RATING WHERE WORKER_ID=ID;

		END IF;

EXCEPTION
	WHEN NO_DATA_FOUND THEN
			DBMS_OUTPUT.PUT_LINE('no data was found');
	WHEN OTHERS THEN
			DBMS_OUTPUT.PUT_LINE('some other exception occurred');


END;
"""

#TODO PROCEDURE CREATE_GROUP_REQUEST

group_request_create = """
CREATE OR REPLACE PROCEDURE CREATE_GROUP_REQUEST(REQ_NO IN NUMBER, USER_ID IN NUMBER)
IS
		WORKER_TYPE VARCHAR2(30);
BEGIN
		SELECT TYPE INTO WORKER_TYPE
		FROM SERVICE_PROVIDER
		WHERE WORKER_ID = USER_ID;

		IF WORKER_TYPE = 'Pest Control Service' THEN
			INSERT INTO GROUP_PEST_CONTROL(ORDER_ID, TEAMLEADER_ID)
      VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO = REQ_NO), USER_ID);

		ELSIF WORKER_TYPE = 'House Shifting Assistant' THEN
			INSERT INTO GROUP_HOUSE_SHIFTING_ASSISTANT(ORDER_ID, TEAMLEADER_ID)
      VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO = REQ_NO), USER_ID);

		ELSIF WORKER_TYPE = 'Electrician' THEN
			INSERT INTO GROUP_ELECTRICIAN(ORDER_ID, TEAMLEADER_ID)
      VALUES( (SELECT ORDER_ID FROM ORDER_INFO WHERE REQUEST_NO = REQ_NO), USER_ID);
		END IF;

EXCEPTION
		WHEN NO_DATA_FOUND THEN
			DBMS_OUTPUT.PUT_LINE('No data found.') ;
		WHEN OTHERS THEN
			DBMS_OUTPUT.PUT_LINE('Unknown Error') ;

END ;
"""

#TODO PROCEDURE ACCEPTING_GROUP_REQUEST

accept_group_req = """
CREATE OR REPLACE PROCEDURE ACCEPTING_GROUP_REQUEST(ORD_ID IN NUMBER, USER_ID IN NUMBER)
IS
		WORKER_TYPE VARCHAR2(30);
		GR_SIZE NUMBER;
		TEAMLEADER NUMBER;
BEGIN
		SELECT TYPE INTO WORKER_TYPE
		FROM SERVICE_PROVIDER
		WHERE WORKER_ID = USER_ID;

		SELECT GROUP_SIZE INTO GR_SIZE
		FROM GROUP_FORM
		WHERE ORDER_ID = ORD_ID;

		IF WORKER_TYPE = 'Electrician' THEN
		    IF GR_SIZE = 0 THEN
                UPDATE GROUP_ELECTRICIAN
                SET WORKER_ID = USER_ID
                WHERE ORDER_ID = ORD_ID;
            ELSIF GR_SIZE = 1 THEN
                UPDATE GROUP_ELECTRICIAN
                SET WORKER_ID_2 = USER_ID
                WHERE ORDER_ID = ORD_ID;
            END IF;

		ELSIF WORKER_TYPE = 'Pest Control Service' THEN
			IF GR_SIZE = 0 THEN
                UPDATE GROUP_PEST_CONTROL
                SET WORKER_ID = USER_ID
                WHERE ORDER_ID = ORD_ID;
            ELSIF GR_SIZE = 1 THEN
                UPDATE GROUP_PEST_CONTROL
                SET WORKER_ID_2 = USER_ID
                WHERE ORDER_ID = ORD_ID;
            END IF;

		ELSIF WORKER_TYPE = 'House Shifting Assistant' THEN
			IF GR_SIZE = 0 THEN
                UPDATE GROUP_HOUSE_SHIFTING_ASSISTANT
                SET WORKER_ID = USER_ID
                WHERE ORDER_ID = ORD_ID;
            ELSIF GR_SIZE = 1 THEN
                UPDATE GROUP_HOUSE_SHIFTING_ASSISTANT
                SET WORKER_ID_2 = USER_ID
                WHERE ORDER_ID = ORD_ID;
            END IF;

		END IF;

        IF GR_SIZE = 0 THEN
            UPDATE GROUP_FORM
            SET GROUP_SIZE = GROUP_SIZE + 1,WORKER_ID = USER_ID
            WHERE ORDER_ID = ORD_ID;
        ELSIF GR_SIZE = 1 THEN
            UPDATE GROUP_FORM
            SET GROUP_SIZE = GROUP_SIZE + 1,WORKER_ID_2 = USER_ID
            WHERE ORDER_ID = ORD_ID;
        END IF;

		SELECT GROUP_SIZE INTO GR_SIZE
		FROM GROUP_FORM
		WHERE ORDER_ID = ORD_ID;

		IF GR_SIZE = 2 THEN
			SELECT TEAM_LEADER_ID INTO TEAMLEADER
			FROM GROUP_FORM
			WHERE ORDER_ID = ORD_ID;

			UPDATE ORDER_INFO
			SET TEAM_LEADER_ID = TEAMLEADER
			WHERE ORDER_ID = ORD_ID;

		END IF;

END ;
"""

#TODO FUNCTION CHECK_IF_GROUP_ALLOWED

check_if_group_allowed = """
CREATE OR REPLACE FUNCTION CHECK_IF_GROUP_ALLOWED(WID IN NUMBER)
RETURN BOOLEAN IS
	WORKER_TYPE VARCHAR2(30);
BEGIN
	SELECT TYPE INTO WORKER_TYPE FROM SERVICE_PROVIDER WHERE WORKER_ID = WID;

	IF LOWER(WORKER_TYPE) = LOWER('ELECTRICIAN') THEN
			RETURN TRUE;
	ELSIF LOWER(WORKER_TYPE) = LOWER('PEST CONTROL SERVICE') THEN
			RETURN TRUE;
	ELSIF LOWER(WORKER_TYPE) = LOWER('HOUSE SHIFTING ASSISTANT') THEN
			RETURN TRUE;
	ELSE
			RETURN FALSE;
	END IF;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN FALSE;
		WHEN OTHERS THEN
		RETURN FALSE;
END ;
/
"""

#TODO TRIGGER INSERT_PAYMENT
trigger_insert_payment = """
CREATE OR REPLACE TRIGGER INSERT_PAYMENT
BEFORE INSERT ON SERVICE_PROVIDER
FOR EACH ROW
BEGIN
		IF :NEW.TYPE = 'Electrician' THEN
			:NEW.PAYMENT_PER_HOUR := 300;
		ELSIF :NEW.TYPE = 'Home Cleaner' THEN
			:NEW.PAYMENT_PER_HOUR := 150;
		ELSIF :NEW.TYPE = 'Pest Control Service' THEN
			:NEW.PAYMENT_PER_HOUR := 500;
		ELSIF :NEW.TYPE = 'Nurse' THEN
			:NEW.PAYMENT_PER_HOUR := 600;
		ELSIF :NEW.TYPE = 'Plumber' THEN
			:NEW.PAYMENT_PER_HOUR := 150;
		ELSIF :NEW.TYPE = 'House Shifting Assistant' THEN
			:NEW.PAYMENT_PER_HOUR := 500;
		ELSIF :NEW.TYPE = 'Carpenter' THEN
			:NEW.PAYMENT_PER_HOUR := 300;
		END IF;

END ;
/
"""

#TODO TRIGGER SET_CUSAPPROVEGRP_TO_FALSE

set_customer_approved_grp_false_bydefault ="""
CREATE OR REPLACE TRIGGER SET_CUSAPPROVEGRP_TO_FALSE
BEFORE INSERT ON GROUP_FORM
FOR EACH ROW
BEGIN
		:NEW.CUSTOMER_APPROVED := 0;

END ;
/
"""

#TODO FUNCTION CHECK_GROUP_EXISTS_AND_APPROVED

check_group_exists_and_approved_customer_order_history = """
CREATE OR REPLACE FUNCTION CHECK_GROUP_EXISTS_AND_APPROVED(OID IN NUMBER)
RETURN NUMBER IS
GOID NUMBER;
CUS NUMBER;
BEGIN
	SELECT ORDER_ID,CUSTOMER_APPROVED INTO GOID,CUS FROM GROUP_FORM WHERE ORDER_ID = OID;
	IF GOID IS NULL THEN
		RETURN 1;
	ELSE
		IF CUS=0 THEN
			RETURN 0;
		ELSIF CUS=1 THEN
			RETURN 1;
		END IF;
	END IF;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 1;
END;
/
"""

#TODO PROCEDURE REJECT_GROUP_REQUEST

reject_group_proc = """
CREATE OR REPLACE PROCEDURE REJECT_GROUP_REQUEST(ORD_ID IN NUMBER)
IS
		WORKER_TYPE VARCHAR2(30);
BEGIN
		SELECT TYPE INTO WORKER_TYPE
		FROM ORDER_INFO
		WHERE ORDER_ID = ORD_ID;
		
		IF WORKER_TYPE = 'Electrician' THEN
			DELETE FROM GROUP_ELECTRICIAN WHERE ORDER_ID = ORD_ID;
			
		ELSIF WORKER_TYPE = 'Pest Control Service' THEN
			DELETE FROM GROUP_PEST_CONTROL WHERE ORDER_ID = ORD_ID;
		
		ELSIF WORKER_TYPE = 'House Shifting Assistant' THEN
			DELETE FROM GROUP_HOUSE_SHIFTING_ASSISTANT WHERE ORDER_ID = ORD_ID;
		
		END IF;
		
		--DELETE FROM ORDER_INFO WHERE ORDER_ID = ORD_ID;
		
		DELETE FROM GROUP_FORM WHERE ORDER_ID = ORD_ID;
		
		UPDATE SERVICE_REQUEST SET ORDER_ID = NULL WHERE ORDER_ID = ORD_ID;
		
		DELETE FROM ORDER_INFO WHERE ORDER_ID = ORD_ID;
		

EXCEPTION
		WHEN NO_DATA_FOUND THEN
			DBMS_OUTPUT.PUT_LINE('No data found.') ;
		WHEN OTHERS THEN
			DBMS_OUTPUT.PUT_LINE('Unknown Error') ;

END ;"""



connection.cursor().execute(calcrating)
print_all_sql(calcrating)

execution = """
BEGIN
	CALCRATING(1,2,'customer');
END ;
"""
connection.cursor().execute(execution)
print_all_sql(execution)
connection.cursor().execute(timediff)
print_all_sql(timediff)
connection.cursor().execute(group_request_create)
print_all_sql(group_request_create)


connection.cursor().execute(accept_group_req)
print_all_sql(accept_group_req)

connection.cursor().execute(check_if_group_allowed)
print_all_sql(check_if_group_allowed)


connection.cursor().execute(set_customer_approved_grp_false_bydefault)
print_all_sql(set_customer_approved_grp_false_bydefault)

connection.cursor().execute(reject_group_proc)
print_all_sql(reject_group_proc)


connection.cursor().execute(check_group_exists_and_approved_customer_order_history)
print_all_sql(check_group_exists_and_approved_customer_order_history)

#
# AREA_LIST_ALL = [
# 'Adabar',
# 'Azampur',
# 'Badda',
# 'Bangsal',
# 'Bimanbandar',
# 'Cantonment ',
# 'Chowkbazar ',
# 'Darus Salam ',
# 'Demra ',
# 'Dhanmondi',
# 'Gendaria',
# 'Gulshan',
# 'Hazaribagh',
# 'Kadamtali',
# 'Kafrul',
# 'Kalabagan',
# 'Kamrangirchar',
# 'Khilgaon',
# 'Khilkhet',
# 'Kotwali',
# 'Lalbagh',
# 'Mirpur Model',
# 'Mohammadpur',
# 'Motijheel',
# 'New Market',
# 'Pallabi',
# 'Paltan',
# 'Panthapath',
# 'Ramna',
# 'Rampura',
# 'Sabujbagh',
# 'Shah Ali',
# 'Shahbag',
# 'Sher-e-Bangla Nagar',
# 'Shyampur',
# 'Sutrapur',
# 'Tejgaon Industrial Area',
# 'Tejgaon',
# 'Turag',
# 'Uttar Khan',
# 'Uttara ',
# 'Vatara',
# 'Wari']
#
# EMERGENCY_TYPE =[
#     'Fire',
#     'Ambulance',
#     'Police'
# ]
#
# PHONE_NUMBER_LIST_FIRE = [
#     '01730002226',
#     '01730002227',
#     '01730002229',
#     '01730002232',
#     '01730002301'
# ]
#
# PHONE_NUMBER_LIST_AMB = [
#     '9556666',
#     '9336611',
#     '9127867',
#     '9125420',
#     '8014476'
# ]
#
# PHONE_NUMBER_LIST_POL = [
#     '01199867799',
#     '01191001155',
#     '01769058053',
#     '01199883723',
#     '01713373162'
# ]
# k=0
# for i in AREA_LIST_ALL :
#     for j in EMERGENCY_TYPE :
#         if j == 'Fire' :
#             phone_number = PHONE_NUMBER_LIST_FIRE[k]
#             k = (k+1)%len(PHONE_NUMBER_LIST_FIRE)
#         elif j == 'Ambulance' :
#             phone_number = PHONE_NUMBER_LIST_AMB[k]
#             k = (k+1)%len(PHONE_NUMBER_LIST_AMB)
#         else :
#             phone_number = PHONE_NUMBER_LIST_POL[k]
#             k = (k + 1) % len(PHONE_NUMBER_LIST_POL)
#         connection.cursor().execute("""
#     INSERT INTO EMERGENCY_PHONE_NUMBER(EMERGENCY_TYPE,PHONE_NUMBER,THANA_NAME) VALUES('"""+j+"""','"""+phone_number+"""','"""+i+"""')""")