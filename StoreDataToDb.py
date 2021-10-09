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
df = pd.read_csv(csv_file_name, encoding= 'raw_unicode_escape')

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
    filename = df.iloc[0][2]
    date = df.iloc[1][2]
    chamber = df.iloc[2][2]
    chamber2 = chamber.split()
    model = " "
    model = model.join(chamber2[:-1])
    serial = chamber2[-1]
    description = df.iloc[3][2]
    software = df.iloc[4][2]
    backgrounds = df.iloc[5][2]
    measurements = df.iloc[6][2]
    trolley = df.iloc[7][2]
    sCD = df.iloc[8][2]
    aperture_wheel = df.iloc[9][2]
    comment = df.iloc[10][2]
    monitorelectrometerrange = df.iloc[11][2]
    monitor_hv = df.iloc[12][2]
    mEFAC_ICElectrometerRange = df.iloc[13][2]
    ic_hv = df.iloc[14][2]
    print(filename)
    #sql="""INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES (Filename,Date,chamber,model,serial,description,software,backgrounds,measurements ,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv)"""
    sql = (
            "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            % (
                filename,
                date,
                chamber,
                model,
                serial,
                description,
                software,
                backgrounds,
                measurements,
                trolley,
                sCD,
                aperture_wheel,
                comment,
                monitorelectrometerrange,
                monitor_hv,
                mEFAC_ICElectrometerRange,
                ic_hv
            )
    )
    #sql = "INSERT INTO header(filename,Date,chamber,model,serial,description) VALUES (('%s','%s','%s','%s','%s','%s')
    # excute sql
    cursor.execute(sql)
    # commit to database
    db.commit()

    df2 = pd.read_csv(csv_file_name, encoding='raw_unicode_escape',skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    #print('kV:',df2.iloc[0]["kV"])
    #print(len(df2))
    sql = "SELECT chamber_ID from header ORDER BY chamber_ID DESC"
    cursor.execute(sql)
    #print(cursor.execute(sql))
    results = cursor.fetchall()
    #print(results)
    chamber_ID = results[0][0]
    print('chamber_ID',chamber_ID)

    for i in range(len(df2)):
        kV = df2.iloc[i]["kV"]
        mA = df2.iloc[i]["mA"]
        barCode = df2.iloc[i]["BarCode"]
        xraysOn = df2.iloc[i]["XraysOn"]
        hVLFilter = df2.iloc[i]["HVLFilter(mm)"]
        filter = df2.iloc[i]["Filter"]
        filter_Ready = df2.iloc[i]["FilterReady"]
        hVLReady = df2.iloc[i]["HVLReady"]
        n = df2.iloc[i]["N"]
        current1 = df2.iloc[i]["Current1(pA)"]
        current2 = df2.iloc[i]["Current2(pA)"]
        p = df2.iloc[i]["P(kPa)"]
        t_MC = df2.iloc[i]["T(MC)"]
        t_Air = df2.iloc[i]["T(Air)"]
        t_SC = df2.iloc[i]["T(SC)"]
        h = df2.iloc[i]["H(%)"]
        sql = (
                "INSERT INTO body(chamber_ID,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                % (
                    chamber_ID,
                    chamber,
                    kV,
                    mA,
                    barCode,
                    xraysOn,
                    hVLFilter,
                    filter,
                    filter_Ready,
                    hVLReady,
                    n,
                    current1,
                    current2,
                    p,
                    t_MC,
                    t_Air,
                    t_SC,
                    h
                )
        )
        #sql = ( "INSERT INTO body(chamber_ID,chamber) values ('%s','%s')" % (chamber_ID,chamber) )
        try:
            # excute sql
            cursor.execute(sql)
            # commit to database
            db.commit()
            print("Processing")
        except:
            # if fail rollback
            db.rollback()
            print("fail")

elif df.iloc[21][0]=="[DATA]":
    print("elif")
    filename = df.iloc[0][2]
    date = df.iloc[1][2]
    chamber = df.iloc[2][2]
    chamber2 = chamber.split()
    model = " "
    model = model.join(chamber2[:-1])
    serial = chamber2[-1]
    description = df.iloc[3][2]
    software = df.iloc[4][2]
    backgrounds = df.iloc[5][2]
    measurements = df.iloc[6][2]
    trolley = df.iloc[7][2]
    sCD = df.iloc[8][2]
    aperture_wheel = df.iloc[9][2]
    comment = df.iloc[10][2]
    monitorelectrometerrange = df.iloc[11][2]
    monitor_hv = df.iloc[12][2]
    mEFAC_ICElectrometerRange = df.iloc[13][2]
    ic_hv = df.iloc[14][2]
    print(filename)

    sql = (
            "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            % (
                filename,
                date,
                chamber,
                model,
                serial,
                description,
                software,
                backgrounds,
                measurements,
                trolley,
                sCD,
                aperture_wheel,
                comment,
                monitorelectrometerrange,
                monitor_hv,
                mEFAC_ICElectrometerRange,
                ic_hv
            )
    )
    try:
        # excute sql
        cursor.execute(sql)
        # commit to database
        db.commit()
    except:
        # if fail rollback
        db.rollback()
        print("fail")
    df2 = pd.read_csv(csv_file_name, encoding='raw_unicode_escape',skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22])
    # print('kV:',df2.iloc[0]["kV"])
    # print(len(df2))

    sql = "SELECT * from header ORDER BY chamber_ID DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    chamber_ID = results[0][0]

    for i in range(len(df2)):
        kV = df2.iloc[i]["kV"]
        mA = df2.iloc[i]["mA"]
        barCode = df2.iloc[i]["BarCode"]
        xraysOn = df2.iloc[i]["XraysOn"]
        hVLFilter = df2.iloc[i]["HVLFilter(mm)"]
        filter = df2.iloc[i]["Filter"]
        filter_Ready = df2.iloc[i]["FilterReady"]
        hVLReady = df2.iloc[i]["HVLReady"]
        n = df2.iloc[i]["N"]
        current1 = df2.iloc[i]["Current1(pA)"]
        current2 = df2.iloc[i]["Current2(pA)"]
        p = df2.iloc[i]["P(kPa)"]
        t_MC = df2.iloc[i]["T(MC)"]
        t_Air = df2.iloc[i]["T(Air)"]
        t_SC = df2.iloc[i]["T(SC)"]
        h = df2.iloc[i]["H(%)"]
        sql = (
                "INSERT INTO body(chamber_ID,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s',%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                % (
                    chamber_ID,
                    chamber,
                    kV,
                    mA,
                    barCode,
                    xraysOn,
                    hVLFilter,
                    filter,
                    filter_Ready,
                    hVLReady,
                    n,
                    current1,
                    current2,
                    p,
                    t_MC,
                    t_Air,
                    t_SC,
                    h,
                )
        )
        try:
            # excute sql
            cursor.execute(sql)
            # commit to database
            db.commit()
            print("Processing")
        except:
            # if fail rollback
            db.rollback()
            print("fail")

print("all the data are stored in database")

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
