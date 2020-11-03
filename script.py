import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_Helping_Hand.settings')
django.setup()


with open('F:\L2-T2\CSE 216\Project\A_Helping_Hand\DDL.txt','r') as file:
    ddl = file.read()

ddl = ddl.replace('\n', ' ').replace('\r', '')
ddl = ddl.replace('\n\n', ' ').replace('\r', '')
print(ddl)
connection.cursor().execute(str(ddl))

OPTIONS = [
        (1, "AC"),
        (2, "TV"),
        (3, "FRIDGE"),
        (4, "GENERAL"),
    ]

for i in OPTIONS:
	connection.cursor().execute(
							"INSERT INTO APPLIANCES(APPLIANCES_ID,TYPE)"
							+ " VALUES ('" + str(i[0]) + "','"  + str(i[1]) + "')")