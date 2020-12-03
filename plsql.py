import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_Helping_Hand.settings')
django.setup()


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
connection.cursor().execute(calcrating)
print(calcrating)

execution = """
BEGIN
	CALCRATING(1,2,'customer');
END ;
"""
connection.cursor().execute(execution)
print(execution)
connection.cursor().execute(timediff)
print(timediff)