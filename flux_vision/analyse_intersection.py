import pandas as pd
import pandasql as ps
from geopy.geocoders import Nominatim
from geopy import distance


# Fonction de modif destypes en valeur int
def mapType(type):
    if type == "Etrangers":
        return 1
    elif type == "Français":
        return 0
    else:
        return 2

# ZONES DIFFERENTES :
# Commune Montreuil
# IRIS 930480204       -> Bas Montreuil Est 4
# IRIS 930480205       -> Bas Montreuil Est 5
# IRIS 930480206       -> Bas Montreuil Est 6
# IRIS 930480401       -> la Noue Clos Francais Guilands 1
# IRIS 930480604       -> Centre Ville Jean Moulin Espoir 4
def mapZone(zone):
    if zone == "IRIS 930480204":
        return "Bas Montreuil Est 4"
    elif zone == "IRIS 930480205":
        return "Bas Montreuil Est 5"
    elif zone == "IRIS 930480206":
        return "Bas Montreuil Est 6"
    elif zone == "IRIS 930480401":
        return "la Noue Clos Francais Guilands 1"
    elif zone == "IRIS 930480604":
        return "Centre Ville Jean Moulin Espoir 4"
    else:
        return "Commune Montreuil"

#Affichage
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', None)

df = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/presence30min-nuitee-communes.csv", sep=';',
                 skipinitialspace=True)
df['Type'] = df.Type.apply(mapType)
df['Zone'] = df.Zone.apply(mapZone)
# print(df.Zone.value_counts().sort_index())

# print("requete start : ")
# dfTravail = ps.sqldf("select * from df where Date>='20/04/2020' and Date<='26/04/2020' and Type=0")
#
# print(dfTravail)

#Plus rapide :
# print("requete start : ")
#je retire Commune monteuil car trop large
dfTravail =  df[(df['Type'] == 0) & (df['Date'] >= "2020-04-20") & (df['Date'] <= "2020-04-26")  & (df['ZoneNuitee'] != -1) & (df.Zone != 'Commune Montreuil')]
dfTravail = dfTravail.sort_values(['Zone', 'Date','Heures'])
print(dfTravail.head(100))


#ZoneNuitee étudiée : 535976 --> Paris
print("================== ETUDE PARIS : ================== ")

dfParisMatin = dfTravail[(dfTravail['ZoneNuitee'] == 535976) & (dfTravail['Heures'] >= '06:00:00') & (dfTravail['Heures'] <= '08:00:00')]
dfParisSoir = dfTravail[(dfTravail['ZoneNuitee'] == 535976) & (dfTravail['Heures'] >= '18:00:00') & (dfTravail['Heures'] <= '20:00:00')]


# print(dfParisMatin)
# print(dfParisSoir)

sumParisMatin = dfParisMatin.groupby(['Date','Zone']).Volume.sum()
sumParisSoir = dfParisSoir.groupby(['Date','Zone']).Volume.sum()

print(sumParisMatin)
print(sumParisSoir)

print("\nVolumes moyens  Matin : ")
print(sumParisMatin.groupby('Zone').mean())
print("\nVolumes moyens  Soir : ")
print(sumParisSoir.groupby('Zone').mean())






