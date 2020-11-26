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
# import datetime
# cur = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(str(cur))
# for row in connection.cursor().execute("select TIMEDIFF2( TO_TIMESTAMP('" + str(cur) +"','YYYY-MM-DD HH24:MI:SS'), REQ_TIME, 'HR') from SERVICE_REQUEST;") :
#     print(row[0])