from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt
from folium import Map
from folium.plugins import HeatMapWithTime
import webbrowser

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
dfTravail =  df[(df['Type'] == 0) & (df['Date'] >= "2020-04-20") & (df['Date'] <= "2020-04-27")  & (df['ZoneNuitee'] != -1) & (df.Zone != 'Commune Montreuil')]
dfTravail = dfTravail.sort_values(['Zone', 'Date','Heures'])
dfTravail.columns = dfTravail.columns.str.strip()
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

print("-------------------------------")
print(dfParisMatin[dfTravail['Date'] == "2020-04-20"])
print("-------------------------------")



dfHisto = pd.read_csv("./../../Data_FluxVisionOrange_AMIF_hackathon/presence30min.csv", sep=';',
                 skipinitialspace=True)
dfHisto['Type'] = dfHisto.Type.apply(mapType)
dfHisto['Zone'] = dfHisto.Zone.apply(mapZone)

dfHisto =  dfHisto[(dfHisto['Type'] == 0) & (dfHisto['Date'] >= "2020-04-20") & (dfHisto['Date'] <= "2020-04-26") & (dfHisto.Zone != 'Commune Montreuil')]
dfHisto = dfHisto.sort_values(['Zone', 'Date','Heures'])

def createHistoVolumeParHeure(df,zone):
    print("\n ================================ : ")
    histo = df.groupby(['Date', 'Zone', 'Heures']).Volume.sum().reset_index()
    print(histo)
    for date in histo.Date.value_counts().sort_index().index:
        histo[(histo['Zone'] == zone) & (histo['Date'] == date)].plot(kind="bar", x="Heures",y="Volume", title=(zone+"-"+date))
        plt.show()
# createHistoVolumeParHeure(dfHisto,"Bas Montreuil Est 4")
createHistoVolumeParHeure(dfTravail[dfTravail['ZoneNuitee'] == 535976],"Bas Montreuil Est 4")
# createHistoVolumeParHeure(dfTravail[dfTravail['ZoneNuitee'] == 535976],"Bas Montreuil Est 5")
# createHistoVolumeParHeure(dfTravail[dfTravail['ZoneNuitee'] == 535976],"Bas Montreuil Est 6")
# createHistoVolumeParHeure(dfTravail[dfTravail['ZoneNuitee'] == 535976],"la Noue Clos Francais Guilands 1")
# createHistoVolumeParHeure(dfTravail[dfTravail['ZoneNuitee'] == 535976],"Centre Ville Jean Moulin Espoir 4")

# HEATMAP :

dfTravail['lat']=0.0
dfTravail['lon']=0.0
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 4"),'lat'] = 48.8580927822
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 4"),'lon'] = 2.43087582343
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 5"),'lat'] = 48.8600096252
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 5"),'lon'] = 2.43575229837
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 6"),'lat'] = 48.858509261
dfTravail.loc[(dfTravail.Zone == "Bas Montreuil Est 6"),'lon'] = 2.43831180464
dfTravail.loc[(dfTravail.Zone == "la Noue Clos Francais Guilands 1"),'lat'] = 48.8614701175
dfTravail.loc[(dfTravail.Zone == "la Noue Clos Francais Guilands 1"),'lon'] = 2.42951750824
dfTravail.loc[(dfTravail.Zone == "Centre Ville Jean Moulin Espoir 4"),'lat'] = 48.8608990488
dfTravail.loc[(dfTravail.Zone == "Centre Ville Jean Moulin Espoir 4"),'lon'] = 2.44076046517


map =  Map(location=[48.861099,2.443600],zoom_start=16)

#print(list(zip(dfTravail.lat, dfTravail.lon, dfTravail.Volume)))
dfHeatMap1J = dfTravail[ (dfTravail['ZoneNuitee'] == 535976)]

dfHeatMap1J.Volume = dfHeatMap1J.Volume / dfHeatMap1J.Volume.max()

index_timestamp = []
for row in dfHeatMap1J.groupby(['Date','Heures']):
    #row[1]  -> Series avec nos 4 lignes, iloc[0] pour recuperer seulement la premiere ligne car les 4 ont le mm timestamp
    #index_timestamp.append([datetime.strptime((row[1].iloc[0]['Date'] + " " +row[1].iloc[0]['Heures']),'%Y-%m-%d %H:%M:%S').timestamp()])
    index_timestamp.append([(row[1].iloc[0]['Date'] + " " +row[1].iloc[0]['Heures'])])

data = []

for _, d in dfHeatMap1J.groupby(['Date','Heures']):
    data.append([[row['lat'], row['lon'], row['Volume']] for _, row in d.iterrows()])
print(index_timestamp)
print(data)


hm_wide = HeatMapWithTime(
    data,
    index = index_timestamp,
    gradient={0.000:'blue',0.1:'green',0.45:'yellow',0.55:'orange',0.7:'red'},
    min_opacity=0.75,
    radius=60,
)

map.add_child(hm_wide)

map.save("map.html")
webbrowser.open("map.html")