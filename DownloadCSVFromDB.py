import csv
import pandas as pd
import pymysql

db = pymysql.connect(host='localhost',user='root',password='password',database='bluering')

cursor = db.cursor()
chamber_ID=19
file = '/tmp/file.csv'

sql = "SELECT * from header WHERE chamber_ID = %s" % chamber_ID

cursor.execute(sql)
rows = cursor.fetchall()

filename = rows[0][2]
date = rows[0][3]
chamber = rows[0][4]
description = rows[0][7]
software = rows[0][8]
backgrounds = rows[0][9]
measurements = rows[0][10]
trolley = rows[0][11]
sDC = rows[0][12]
aperturewheel = rows[0][13]
comment = rows[0][14]
monitorelectrometerrange = rows[0][15]
monitorhv = rows[0][16]
mEFAC_ICElectrometerRange = rows[0][17]
ic_hv = rows[0][18]
clientname = rows[0][19]
address1 = rows[0][20]
address2 = rows[0][21]
operator = rows[0][22]
calnumber = rows[0][23]

with open(file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['[COMET X-RAY MEASUREMENT]'])
    writer.writerow(['Filename','',filename])
    writer.writerow(['Date','',date])
    writer.writerow(['Chamber', '', chamber])
    writer.writerow(['Description', '', description])
    writer.writerow(['Software', '', software])
    writer.writerow(['Backgrounds', '', backgrounds])
    writer.writerow(['Measurements', '', measurements])
    writer.writerow(['Trolley (mm)', '', trolley])
    writer.writerow(['SCD (mm)', '', sDC])
    writer.writerow(['Aperture wheel', '', aperturewheel])
    writer.writerow(['Comment', '', comment])
    writer.writerow(['Monitor electrometer range', '', monitorelectrometerrange])
    writer.writerow(['Monitor HV', '', monitorhv])
    writer.writerow(['MEFAC-IC electrometer range', '', mEFAC_ICElectrometerRange])
    writer.writerow(['IC HV', '', ic_hv])
    writer.writerow(['Client name', '', clientname])
    writer.writerow(['Address 1', '', address1])
    writer.writerow(['Address 2', '', address2])
    writer.writerow(['Operator', '', operator])
    writer.writerow(['CAL Number', '', calnumber])
    writer.writerow(['[DATA]'])
    writer.writerow(['kV','mA','BarCode','XraysOn','HVLFilter(mm)','Filter','FilterReady','HVLReady','N','Current1(pA)','Current2(pA)','P(kPa)','T(MC)','T(Air)','T(SC)','H(%)'])

#sql = "SELECT * from body WHERE chamber_ID = %s" % chamber_ID
sql = "SELECT kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H from body WHERE chamber_ID = %s" % chamber_ID

cursor.execute(sql)
rows = cursor.fetchall()
fp = open(file, 'a')
myFile = csv.writer(fp)
myFile.writerows(rows)
fp.close()

db.close()
