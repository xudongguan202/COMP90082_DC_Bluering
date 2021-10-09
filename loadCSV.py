#import pymysqld
import pandas as pd


def MC2(row, BgdMC2_Before_Lab):
    MC2=row["Current1(pA)"]-BgdMC2_Before_Lab
    return MC2

def IC2(row,BgdIC2_Before_Lab,BgdMC2_Before_Lab):
    MC2=(row["Current2(pA)"]-BgdIC2_Before_Lab)/(row["Current1(pA)"]-BgdMC2_Before_Lab)
    return MC2

def TM2(row):
    MC2=row["T(MC)"]
    return MC2


def TS2(row):
    MC2=row["T(SC)"]
    return MC2

def H2(row):
    MC2=row["H(%)"]
    return MC2



df_Client = pd.read_csv("Raw MEX measurement data 1Client.csv", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21])
df_Lab = pd.read_csv("Raw MEX measurement data 1Lab.csv", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

headLab = pd.read_csv('Raw MEX measurement data 1Lab.csv', usecols=[2], nrows=17)
headClient = pd.read_csv('Raw MEX measurement data 1Client.csv', usecols=[2], nrows=17)



#提取Client基本信息
chamberID_Client=headClient.iat[2,0]
chamberID_Lab=headLab.iat[2,0]
clientName=headClient.iat[15,0]
clientAddress=headClient.iat[16,0]


measurmens_Client = headClient.iat[6,0]
measurmens_Client = headClient.iat[5,0]
measurmens_Lab = headLab.iat[6,0]
backgroud_Lab = headLab.iat[5,0]
xAxisList = df_Client["kV"].unique()
filterName = df_Client["Filter"].unique()

current1_Client=df_Client["Current1(pA)"]
current2_Client=df_Client["Current2(pA)"]

current1_Lab=df_Lab["Current1(pA)"]
current2_Lab=df_Lab["Current2(pA)"]

BgdIC1_Before_Client=current1_Client.iloc[0:89].mean(axis=0)
BgdMC1_Before_Client=current2_Client.iloc[0:89].mean(axis=0)

BgdIC2_Before_Lab=current1_Lab.iloc[0:89].mean(axis=0)
BgdMC2_Before_Lab=current2_Lab.iloc[0:89].mean(axis=0)


df_Client["R1"]=(((df_Client["Current2(pA)"]-BgdIC2_Before_Lab)/(df_Client["Current1(pA)"]-BgdMC2_Before_Lab)).groupby([df_Client['Filter'], df_Client['XraysOn']]).transform('mean').round(5))
df_Lab["R2"]=(((df_Lab["Current2(pA)"]-BgdIC2_Before_Lab)/(df_Lab["Current1(pA)"]-BgdMC2_Before_Lab)).groupby([df_Lab['Filter'], df_Lab['XraysOn']]).transform('mean').round(5))




#currentLab_Mean["H2"]=currentLab_Mean.apply(H2,axis=1)
pd.set_option('display.max_rows', None)

group_Client=df_Client.groupby(["Filter", "XraysOn"], as_index=False)
df_Client_MEX=group_Client.agg({"kV": "mean", "Current1(pA)": "mean", "Current2(pA)": "mean","T(MC)": "mean","T(Air)": "mean", "R1": "mean"})

group_Lab=df_Lab.groupby(["Filter", "XraysOn"], as_index=False )
df_Lab_MEX=group_Lab.agg({"kV": "mean", "Current1(pA)": "mean", "Current2(pA)": "mean", "T(MC)": "mean", "T(SC)": "mean", "H(%)": "mean",  "R2": "mean"})
df_Client_MEX["R2"]=df_Lab_MEX["R2"]
df_Lab_MEX["MC2"]=df_Lab_MEX[["Current1(pA)"]].apply(lambda x:x["Current1(pA)"]-BgdMC2_Before_Lab,axis=1)
df_Lab_MEX["IC2"]=df_Lab_MEX[["Current2(pA)"]].apply(lambda x:x["Current2(pA)"]-BgdIC2_Before_Lab,axis=1)

df_Client_MEX["MC1"]=df_Lab_MEX[["Current1(pA)"]].apply(lambda x:x["Current1(pA)"]-BgdMC1_Before_Client,axis=1)
df_Client_MEX["IC1"]=df_Lab_MEX[["Current2(pA)"]].apply(lambda x:x["Current2(pA)"]-BgdIC1_Before_Client,axis=1)
df_Client_MEX["MC2"]=df_Lab_MEX["MC2"]
df_Client_MEX["IC2"]=df_Lab_MEX["IC2"]
df_Client_MEX["TM2"]=df_Lab_MEX["T(MC)"]
df_Client_MEX["TS2"]=df_Lab_MEX["T(SC)"]
df_Client_MEX["H2"]=df_Lab_MEX["H(%)"]

Ma = 6.18E-06
WE = 33.97


#df_Client_MEX["NK"]=df_Lab_MEX[["Current2(pA)"]].apply(lambda x:x["Current2(pA)"]-BgdIC1_Before_Client,axis=1)

product = pd.read_csv("KKMaWE.csv", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

product = product[['Filter', 'Product']]

#MEX report
MEXs = pd.read_csv("KKMaWE.csv", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
MEX = MEXs[['Filter', '(kV)', 'mm Al', 'mm Cu', '(mm Al)', '(mm Cu)', '(eff, Cu)', 'Air kerma rate']]




df_merge_col = pd.merge(df_Client_MEX, product, on='Filter')
df_merge_col["NK"]=df_merge_col[["Product","R1","R2","T(Air)","H2","T(MC)","TS2","TM2"]].apply(lambda x:x["R2"]*WE*x["Product"]*((273.15+x["TS2"])/(273.15+x["TM2"]))*(0.995766667+0.000045*x["H2"])/(Ma*x["R1"]*(273.15+x["T(Air)"])/(273.15+x["T(MC)"]))/1000000,axis=1)

df_merge_col = df_merge_col.drop(df_merge_col[df_merge_col.XraysOn ==False].index)

KeV=df_merge_col["kV"].values.tolist()
Beam=df_merge_col["Filter"].values.tolist()
NK=df_merge_col["NK"].values.tolist()

df_merge_col=pd.merge(df_merge_col, MEX, on='Filter')
MEXreport=df_merge_col[['Filter', '(kV)', 'mm Al', 'mm Cu', '(mm Al)', '(mm Cu)', '(eff, Cu)','NK', 'Air kerma rate']]
MEXreport['U']= 1.4
MEXreport_sortByKev=MEXreport.sort_values(by=['(kV)'])

MEXreport_PTB=MEXreport.loc[(MEXreport['Filter'].isin(['NXA50','NXA70','NXB100','NXC120','NXD140','NXE150','NXF200','NXG250','NXH280','NXH300','NXH300*']))]

MEXreport_sortByKev_NX = MEXreport.loc[MEXreport['Filter'].str.contains('NX')]
MEXreport_sortByKev_NX = MEXreport_sortByKev_NX.sort_values(by=['(kV)'])

print(MEXreport_sortByKev_NX)




