from ftp.ftp import *
import json
import mysql.connector
import time
import datetime
from helpers.helpers import *

HOSTNAME = ""
USERNAME = ""
PASSWORD = ""
WEBSITE  = "website1"

ftp = MyFtp(HOSTNAME, USERNAME, PASSWORD)

login_result = ftp.Connect()
print(login_result)
print(ftp.GetWelcome())

print('---------------------------------------------------------')

with open(Helpers.GetCurDir() + "\\storage\\websites\\" + WEBSITE + "\\map.json" , 'w') as f:
    json.dump(ftp.GetServerFiles(""), f)

for data in ftp.GetServerFiles(""):
    if data['type'] == "dir":
        Helpers.CreateDir(Helpers.GetCurDir() + "\\storage\\websites\\" + WEBSITE + "\\" + data['path'])
    else:
        if data['path']:
            file = data['path'] + "//" + data['file']
        else:
            file = data['file']
        ftp.DownloadFile(file, Helpers.GetCurDir() + "\\storage\\websites\\" + WEBSITE + "\\" + data['path'] + data['file'])


