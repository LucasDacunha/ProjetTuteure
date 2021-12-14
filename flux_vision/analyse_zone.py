import pandas as pd
import pandasql as ps
from geopy.geocoders import Nominatim
from geopy import distance
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

def calculLatLon(address,index):
    location = geolocator.geocode(address + ", France")
    if (index == 535693):
        addr = (48.863812, 2.448451)
    else:
        addr = (location.latitude, location.longitude)
    return addr

def calculDistance(addr1,addr2):
    return distance.distance(addr1, addr2).km

def calculDistanceMoy(addr1,df,typeDico,dico):
    sommeDist = 0
    for i in range(0, len(df.index)):
        if(df.index[i] != -1):
            # print(" i : "+str(i)+" => "+str(df.index[i]))
            address = getLabelZoneFromId(df.index[i], typeDico, dico)
            addr2 = calculLatLon(address, df.index[i])
            sommeDist += (calculDistance(addr1, addr2) * df.values[i])

    return sommeDist/df.values.sum()





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

addr1 = (48.863812, 2.448451) #coordoonées montreuil

def calculDistanceApply(zoneId):
    if(zoneId != -1):
        address = getLabelZoneFromId(zoneId, typeDico, dico)
        addr2 = calculLatLon(address, zoneId)
        return calculDistance(addr1, addr2)


print("\n======== Zones_Activite diff en tout : ========")
vcZoneAct = zoneMontreuil.ZoneActivite.value_counts()
print(vcZoneAct)
print("======== Commune majoritaire : ")
address = getLabelZoneFromId(vcZoneAct.index[0],typeDico,dico)
print(str(vcZoneAct.index[0]) +" "+ address + " : "+ str(vcZoneAct.values[0])) #400479
addr2 = calculLatLon(address,vcZoneAct.index[0])
print("Lat,Lon : "+str(addr2))
print("distance zone etu : "+ str(calculDistance(addr1, addr2))+ " km")

print("======== Commune minoritaire : ")
lastrow = len(vcZoneAct)-1
address = getLabelZoneFromId(vcZoneAct.index[lastrow],typeDico,dico)
print(str(vcZoneAct.index[lastrow]) +" "+ address + " : "+ str(vcZoneAct.values[lastrow])) #401629
addr2 = calculLatLon(address,vcZoneAct.index[lastrow])
print("Lat,Lon : "+str(addr2))
print("distance zone etu : "+ str(calculDistance(addr1, addr2))+ " km")
print("======== Distance moyenne 20 premiers : ")
print(calculDistanceMoy(addr1,vcZoneAct.head(20),typeDico,dico))
print("======== Distance moyenne 20 derniers : ")
print(calculDistanceMoy(addr1,vcZoneAct.tail(20),typeDico,dico))
# frameVcZoneAct = vcZoneAct.to_frame().index.to_frame()
# moy = frameVcZoneAct[0].apply(calculDistanceApply)
# print(moy)


print("\n======== Zones_Nuitee diff en tout : ========")
vcZoneNuit = zoneMontreuil.ZoneNuitee.value_counts()
print(vcZoneNuit)
print("======== Commune majoritaire : ")
address = getLabelZoneFromId(vcZoneNuit.index[0],typeDico,dico)
print(str(vcZoneNuit.index[0]) +" "+ address + " : "+ str(vcZoneNuit.values[0])) #400479
addr2 = calculLatLon(address,vcZoneNuit.index[0])
print("Lat,Lon : "+str(addr2))
print("distance zone etu : "+ str(calculDistance(addr1, addr2))+ " km")

print("======== Commune minoritaire : ")
lastrow = len(vcZoneNuit)-1
address = getLabelZoneFromId(vcZoneNuit.index[lastrow],typeDico,dico)
print(str(vcZoneNuit.index[lastrow]) +" "+ address + " : "+ str(vcZoneNuit.values[lastrow])) #401450
addr2 = calculLatLon(address,vcZoneNuit.index[lastrow])
print("Lat,Lon : "+str(addr2))
print("distance zone etu : "+ str(calculDistance(addr1, addr2))+ " km")
print("======== Distance moyenne 20 premier : ")
print(calculDistanceMoy(addr1,vcZoneNuit.head(20),typeDico,dico))
print("======== Distance moyenne 20 derniers : ")
print(calculDistanceMoy(addr1,vcZoneNuit.tail(20),typeDico,dico))




