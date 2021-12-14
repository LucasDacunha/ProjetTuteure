import pandas as pd
import pandasql as ps
import numpy as np
from matplotlib import pyplot as plt
import os




# print(os.getcwd())

# Fonction de modif destypes en valeur int
def mapType(type):
    if type == "Etrangers":
        return 1
    elif type == "Français":
        return 0
    else:
        return 2


# Fonction de modif des durées en valeur int
def mapDuree(duree):  #
    if duree == "Inf30min":
        return 0
    elif duree == "30min3h":
        return 1
    elif duree == "Sup3h":
        return 2
    else:
        return 3


# Fonction de découpe des datas par zone
def decoupeZone(df):
    dfListe = []
    dfListe.append(df[df['Zone'] == "Commune Montreuil"])
    currentZone = "Commune Montreuil"

    for i in range(1, len(df.index)):
        if (df.loc[i - 1, "Zone"] != currentZone):
            print("nouvelle zone")
            currentZone = df.loc[i - 1, "Zone"]
            dfListe.append(df[df['Zone'] == currentZone])

    return dfListe


df = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/presencejournee.csv", sep=';',
                 skipinitialspace=True)
# df = pd.read_csv("./drive/MyDrive/Projet_heatMap/Data_FluxVision_AMIF_hackathon/presence30min.csv",sep=';',skipinitialspace=True)

df['Type'] = df.Type.apply(mapType)
df['Duree'] = df.Duree.apply(mapDuree)
# df['Date'] =  pd.to_datetime(df['Date'], format='%d%b%Y:%H:%M:%S.%f')   # DEJA FAIT PAR PANDAS


print("\n INFO GENERALES : ")
print("\n Head (20) :")
print(df.head(20))

print("\n Types : ")
print(df.dtypes)

dfListe = decoupeZone(df)
print(len(dfListe))
# for i in range(0,len(dfListe)):
#   print("\n === Separation Zone ===")
#   print(dfListe[i])

print("\n========================================")
print("\n Graf par zone : ")

for i in range(0, len(dfListe)):
    print("\n Graf freq date (RAW) : ZONE {}".format(i))
    # dfListe[i].plot(x='Date', y='Volume', kind='line') # type possible : scatter , line , bar(BAR LONG A COMPIL)
    # plt.show()

print("\n========================================")
print("\n Tableau Karnaugh : ")
print("\n Pour le 2020-04-20, resté + de 3h")

maxValueFRZone1 = \
dfListe[0][((dfListe[0]['Type'] == 0) & (dfListe[0]['Date'] == "2020-04-20") & (dfListe[0]['Duree'] == 2))][
    'Volume'].max()  # Where condition (where type = 0 ==> where type = francais)
# minValueFRZone1 = dfListe[0][((dfListe[0]['Type']==0) & (dfListe[0]['Date']=="2020-04-20") & (dfListe[0]['Duree']==2))]['Volume'].min()

maxValueFRZone2 = \
dfListe[1][((dfListe[1]['Type'] == 0) & (dfListe[1]['Date'] == "2020-04-20") & (dfListe[1]['Duree'] == 2))][
    'Volume'].max()
# minValueFRZone2 = dfListe[1][((dfListe[1]['Type']==0) & (dfListe[1]['Date']=="2020-04-20") & (dfListe[1]['Duree']==2))]['Volume'].min()

# print("\n Max / min value Zone 1 :")
# print(maxValueFRZone1)
# print("/")
# print(minValueFRZone1)

# print("\n Max / min value Zone 2 :")
# print(maxValueFRZone2)
# print("/")
# print(minValueFRZone2)

upperBoundFR = max(maxValueFRZone1, maxValueFRZone2)
lowerBoundFR = min(maxValueFRZone1, maxValueFRZone2)

print("\n upper / lower FR:")
print(upperBoundFR)
print("/")
print(lowerBoundFR)

maxValueETZone1 = \
dfListe[0][((dfListe[0]['Type'] == 1) & (dfListe[0]['Date'] == "2020-04-20") & (dfListe[0]['Duree'] == 2))][
    'Volume'].max()  # Where condition (where type = 0 ==> where type = francais)
maxValueETZone2 = \
dfListe[1][((dfListe[1]['Type'] == 1) & (dfListe[1]['Date'] == "2020-04-20") & (dfListe[1]['Duree'] == 2))][
    'Volume'].max()

upperBoundET = max(maxValueETZone1, maxValueETZone2)
lowerBoundET = min(maxValueETZone1, maxValueETZone2)

print("\n upper / lower ET:")
print(upperBoundET)
print("/")
print(lowerBoundET)

# LP :


# Table verite :
# X      | Zone1           | !Zone1
# Zone2  |     ?           | maxValueFRZone2
# !Zone2 | maxValueFRZone1 | osef ?

print("\n ==================== TEST TABLEAU MANUEL")

# df2 = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/presencejournee-activitenuitee-bassindevie.csv", sep=';',
#                  skipinitialspace=True)
# df2['Type'] = df2.Type.apply(mapType)
# df2['Duree'] = df2.Duree.apply(mapDuree)
#
# dfJ1 = ps.sqldf("select * from df2 where Type=0 and Zone='Commune Montreuil' and Date='2020-04-20' and Duree=2 and ZoneActivite=400479")
# print("========================= DF J1 : ")
# print(dfJ1)
#
# print("========================= DF J2 : ")
# dfJ2 = ps.sqldf("select * from df2 where Type=0 and Zone='Commune Montreuil' and Date='2020-04-21' and Duree=2 and ZoneActivite=400479")
# print(dfJ2)


