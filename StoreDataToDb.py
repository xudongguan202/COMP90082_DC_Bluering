import csv
import pandas as pd
import pymysql

#key in your password
db = pymysql.connect(host='localhost',user='root',password='password',database='bluering')

cursor = db.cursor()
#Demo
#csv_file_name = 'description/data2/CAL00001 Raw ClientA-Run1-Client.csv'
csv_file_name = 'description/data/Raw MEX measurement data 1Client.csv'
#df = pd.read_csv('description/data/Raw MEX measurement data 1Client.csv', encoding= 'unicode_escape')
df = pd.read_csv(csv_file_name, encoding= 'unicode_escape')

#print(df.iloc[0][2])
print(df.iloc[21][0])

print('Filename',df.iloc[0][2])
print('Date',df.iloc[1][2])
chamber=df.iloc[2][2]
print('chamber:',chamber)
chamber=chamber.split()
model=' '
model=model.join(chamber[:-1])
print('model:',model)
print('serial:',chamber[-1])
print('Description:',df.iloc[3][2])

# SQL 插入语句
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,LAST_NAME, AGE, SEX, INCOME)
#          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
if df.iloc[15][0]=="[DATA]":
    Filename = df.iloc[0][2]
    Date = df.iloc[1][2]
    chamber = df.iloc[2][2]
    chamber2 = chamber.split()
    model = ' '
    model = model.join(chamber2[:-1])
    serial = chamber2[-1]
    description = df.iloc[3][2]
    software = df.iloc[4][2]
    backgrounds = df.iloc[5][2]
    measurements = df.iloc[6][2]
    Trolley = df.iloc[7][2]
    SCD = df.iloc[8][2]
    aperturewheel = df.iloc[9][2]
    Comment = df.iloc[10][2]
    monitorelectrometerrange = df.iloc[11][2]
    monitorhv = df.iloc[12][2]
    MEFAC_ICElectrometerRange = df.iloc[13][2]
    ic_hv = df.iloc[14][2]
    print(Filename)
    #sql="""INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES (Filename,Date,chamber,model,serial,description,software,backgrounds,measurements ,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv)"""
    sql = "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv)
    #sql = "INSERT INTO header(filename,Date,chamber,model,serial,description) VALUES (('%s','%s','%s','%s','%s','%s')
    # excute sql
    cursor.execute(sql)
    # commit to database
    db.commit()

    df2 = pd.read_csv(csv_file_name, encoding='unicode_escape',skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    #print('kV:',df2.iloc[0]["kV"])
    #print(len(df2))
    for i in range(len(df2)):
        kV = df2.iloc[i]["kV"]
        mA = df2.iloc[i]["mA"]
        BarCode = df2.iloc[i]["BarCode"]
        XraysOn = df2.iloc[i]["XraysOn"]
        HVLFilter = df2.iloc[i]["HVLFilter(mm)"]
        Filter = df2.iloc[i]["Filter"]
        FilterReady = df2.iloc[i]["FilterReady"]
        HVLReady = df2.iloc[i]["HVLReady"]
        N = df2.iloc[i]["N"]
        Current1 = df2.iloc[i]["Current1(pA)"]
        Current2 = df2.iloc[i]["Current2(pA)"]
        P = df2.iloc[i]["P(kPa)"]
        T_MC = df2.iloc[i]["T(MC)"]
        T_Air = df2.iloc[i]["T(Air)"]
        T_SC = df2.iloc[i]["T(SC)"]
        H = df2.iloc[i]["H(%)"]
        sql = "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Filename,chamber,kV,mA,BarCode,XraysOn,HVLFilter,Filter,FilterReady,HVLReady,N,Current1,Current2,P,T_MC,T_Air,T_SC,H)
        # excute sql
        cursor.execute(sql)
        # commit to database
        db.commit()

elif df.iloc[21][0]=="[DATA]":
    print("elif")
    Filename = df.iloc[0][2]
    Date = df.iloc[1][2]
    chamber = df.iloc[2][2]
    chamber2 = chamber.split()
    model = ' '
    model = model.join(chamber2[:-1])
    serial = chamber2[-1]
    description = df.iloc[3][2]
    software = df.iloc[4][2]
    backgrounds = df.iloc[5][2]
    measurements = df.iloc[6][2]
    Trolley = df.iloc[7][2]
    SCD = df.iloc[8][2]
    aperturewheel = df.iloc[9][2]
    Comment = df.iloc[10][2]
    monitorelectrometerrange = df.iloc[11][2]
    monitorhv = df.iloc[12][2]
    MEFAC_ICElectrometerRange = df.iloc[13][2]
    ic_hv = df.iloc[14][2]
    clientname = df.iloc[15][2]
    address1 = df.iloc[16][2]
    address2 = df.iloc[17][2]
    operator = df.iloc[18][2]
    calnumber = df.iloc[19][2]
    sql = "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv,clientname,address1,address2,operator,calnumber) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv,clientname,address1,address2,operator,calnumber)
    try:
        # excute sql
        cursor.execute(sql)
        # commit to database
        db.commit()
    except:
        # if fail rollback
        db.rollback()
        print("fail")
    df2 = pd.read_csv(csv_file_name, encoding='unicode_escape',skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22])
    # print('kV:',df2.iloc[0]["kV"])
    # print(len(df2))
    for i in range(len(df2)):
        kV = df2.iloc[i]["kV"]
        mA = df2.iloc[i]["mA"]
        BarCode = df2.iloc[i]["BarCode"]
        XraysOn = df2.iloc[i]["XraysOn"]
        HVLFilter = df2.iloc[i]["HVLFilter(mm)"]
        Filter = df2.iloc[i]["Filter"]
        FilterReady = df2.iloc[i]["FilterReady"]
        HVLReady = df2.iloc[i]["HVLReady"]
        N = df2.iloc[i]["N"]
        Current1 = df2.iloc[i]["Current1(pA)"]
        Current2 = df2.iloc[i]["Current2(pA)"]
        P = df2.iloc[i]["P(kPa)"]
        T_MC = df2.iloc[i]["T(MC)"]
        T_Air = df2.iloc[i]["T(Air)"]
        T_SC = df2.iloc[i]["T(SC)"]
        H = df2.iloc[i]["H(%)"]
        sql = "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Filename, chamber, kV, mA, BarCode, XraysOn, HVLFilter, Filter, FilterReady, HVLReady, N, Current1, Current2, P,T_MC, T_Air, T_SC, H)
        try:
            # excute sql
            cursor.execute(sql)
            # commit to database
            db.commit()
            print("success")
        except:
            # if fail rollback
            db.rollback()
            print("fail")

# try:
#     # excute sql
#     cursor.execute(sql)
#     # commit to database
#     db.commit()
#     print("success")
# except:
#     # if fail rollback
#     db.rollback()
#     print("fail")

# close connection
db.close()
