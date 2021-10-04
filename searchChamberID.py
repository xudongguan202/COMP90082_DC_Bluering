import csv
import pandas as pd
import pymysql

db = pymysql.connect(host='localhost',user='root',password='Bluering123.',database='bluering')

cursor = db.cursor()

job_number = 10
chamber = 'PTW 30013 5122'
clientname = 'ClientA_Name'

#sql = "SELECT chamber_ID from header WHERE job_number = %s" % job_number
#sql = "SELECT chamber_ID from header WHERE chamber = %s" % chamber
#sql = "SELECT chamber_ID from header WHERE job_number = %s AND chamber = '%s'" % (job_number,chamber)
sql = "SELECT b.chamber_ID, b.chamber, a.job_number, a.clientname FROM client a RIGHT JOIN header b ON a.job_number = b.job_number WHERE LOWER(a.clientname) = '%s'"\
      % (clientname.lower())

cursor.execute(sql)
rows = cursor.fetchall()

result = []

for row in rows:
    result.append(row)

print(result)

db.close()
