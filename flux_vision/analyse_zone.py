import pandas as pd
import pandasql as ps
from geopy.geocoders import Nominatim
import numpy as np
from matplotlib import pyplot as plt

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

def selectDfWhere(type : int, zone : str, duree : int, df1):
    data = ps.sqldf("select * from df1 where Type="+str(type)+" and Zone='"+zone+"' and Duree="+str(duree))
    return data

def getLabelZoneFromId(id : int, typeDico : int, df1):
    if(typeDico == 0):
        return df1.Label[df1.ID_BassinDeVie == id].item()
    elif(typeDico == 1):
        return df1.Label[df1.ID_Commune_groupement == id].item()
    elif(typeDico == 2):
        return df1.Label[df1.ID_Iris_groupement == id].item()
    else:
        return "ERREUR TYPE DICO"



df = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/presencejournee-activitenuitee-communes.csv", sep=';',
                 skipinitialspace=True)
dico = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/Dictionnaire_Label_Zones_Communes.csv", sep=';',
                 skipinitialspace=True, encoding='latin-1')
typeDico = 1

geolocator = Nominatim(user_agent="MonNom")

df['Type'] = df.Type.apply(mapType)
df['Duree'] = df.Duree.apply(mapDuree)


zoneMontreuil = selectDfWhere(0,"Commune Montreuil",2,df)
print("============== Français dans la Zone : Commune Montreuil pour une duree Sup3h ==============")
print(zoneMontreuil.head(20))
print("Nombre ligne : ")
print(len(zoneMontreuil))



print("\n======== Zones_Activite diff en tout : ========")
vcZoneAct = zoneMontreuil.ZoneActivite.value_counts()
print(vcZoneAct)
print("======== Commune majoritaire : ")
address = getLabelZoneFromId(vcZoneAct.index[0],typeDico,dico)
print(str(vcZoneAct.index[0]) +" "+ address + " : "+ str(vcZoneAct.values[0])) #400479
location = geolocator.geocode(address)
print("Lat,Lon : "+str((location.latitude, location.longitude)))

print("======== Commune minoritaire : ")
lastrow = len(vcZoneAct)-1
address = getLabelZoneFromId(vcZoneAct.index[lastrow],typeDico,dico)
print(str(vcZoneAct.index[lastrow]) +" "+ address + " : "+ str(vcZoneAct.values[lastrow])) #401629
location = geolocator.geocode(address)
print("Lat,Lon : "+str((location.latitude, location.longitude)))



print("\n======== Zones_Nuitee diff en tout : ========")
vcZoneNuit = zoneMontreuil.ZoneNuitee.value_counts()
print(vcZoneNuit)
print("======== Commune majoritaire : ")
address = getLabelZoneFromId(vcZoneNuit.index[0],typeDico,dico)
print(str(vcZoneNuit.index[0]) +" "+ address + " : "+ str(vcZoneNuit.values[0])) #400479
location = geolocator.geocode(address)
print("Lat,Lon : "+str((location.latitude, location.longitude)))

print("======== Commune minoritaire : ")
lastrow = len(vcZoneNuit)-1
address = getLabelZoneFromId(vcZoneNuit.index[lastrow],typeDico,dico)
print(str(vcZoneNuit.index[lastrow]) +" "+ address + " : "+ str(vcZoneNuit.values[lastrow])) #401450
location = geolocator.geocode(address)
print("Lat,Lon : "+str((location.latitude, location.longitude)))




