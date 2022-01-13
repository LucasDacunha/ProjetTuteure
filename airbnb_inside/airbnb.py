import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Point, LineString, Polygon, shape
from folium import Map, Marker, Icon,Figure
import folium
from IPython.display import display
import webbrowser

# from google.colab import drive
# drive.mount._DEBUG = True
# # print(getpass.getpass())
# drive.mount('/content/drive')

my_path = "/AirbnbInside" # THIS is your GDrive path
# gdrive_path = "/content/drive" + "/My Drive" + my_path
gdrive_path = "C:/Users/matte/Desktop/projetTut/AirbnbInside" # pour pc

# /content/drive/My Drive/folders/my_folder_name

listing_input_file = gdrive_path + "/bordeaux/listings.csv" # The specific file you are trying to access
rawdata = pd.read_csv(listing_input_file)

# items=['host_name', 'last_scraped','neighbourhood_cleansed','neighbourhood_group_cleansed','latitude','longitude']

# print(rawdata.filter(items=['id','last_scraped','neighbourhood_cleansed','latitude','longitude']).head(30))

# On regroupe les données suivant le quartier
def decoupeZone(rawdata):  
  dfListe = []
  quartierFait = []
  quartierCourant = ""

  for i in range(1,len(rawdata.index)):
    if(rawdata.loc[i-1,"neighbourhood_cleansed"] not in quartierFait):
      quartierCourant = rawdata.loc[i-1,"neighbourhood_cleansed"]
      quartierFait.append(quartierCourant)
      dfListe.append(rawdata[rawdata['neighbourhood_cleansed']==quartierCourant])
  liste= []
  liste.append(dfListe)
  liste.append(quartierFait)
  return liste


# dfListe = decoupeZone(rawdata.filter(items=['id','last_scraped','neighbourhood_cleansed','latitude','longitude']))
# print(dfListe[1])
def appartParQuartier(dfListe):
  nbAppartParQuartier = []
  for i in range(0,len(dfListe[0])):
    # print("======================== "+dfListe[1][i]+" ========================")
    # print(dfListe[0][i])
    nbAppartParQuartier.append(len(dfListe[0][i]))
  return nbAppartParQuartier

# nbAppartParQuartier = []
# for i in range(0,len(dfListe[0])):
#   nbAppartParQuartier.append(len(dfListe[0][i]))
# nbAppartParQuartier = appartParQuartier(dfListe)
# le graph ne marche plus pour une raison inconnue je n'ai pas modifier le code
# fig, ax = plt.subplots(figsize=(10,15))
# ax.barh(dfListe[1], nbAppartParQuartier)
# plt.show()

# review_input_file = gdrive_path + "/bordeaux/reviews.csv"
# reviewData = pd.read_csv(review_input_file)

def findLatLongFromAppartId(id,rawdata):
  latLong = []
  for i in range(1,len(rawdata.index)):
    if(rawdata.loc[i-1,"id"]==id):
      latLong.append(str(rawdata.loc[i-1,"latitude"]))
      latLong.append(str(rawdata.loc[i-1,"longitude"]))
      break
  return latLong 

# latLong = findLatLongFromAppartId(317658,rawdata)
# print("trouve :"+latLong[0]+" ; "+latLong[1])

def positionClient(reviewData,rawdata,year,withYear):
  if(withYear):
    start_date = str(year)+"-01-01"
    end_date = str(year)+"-12-31"
    after_start_date = reviewData["date"] >= start_date
    before_end_date = reviewData["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    reviewData = reviewData.loc[between_two_dates]
  # print(reviewData)
  reviewer_ids = []
  reviewer_names = []
  listing_ids = []
  dates = []
  latitudes = []
  longitudes = []
  # reviewData.reset_index() # marche pas
  # print(reviewData.index)
  for i in reviewData.index: # car les index ne sont pas un range de 0 à X (1,2,3,...,X)
    idAppart=reviewData.loc[i,"listing_id"]
    reviewer_ids.append(reviewData.loc[i,"reviewer_id"])
    reviewer_names.append(reviewData.loc[i,"reviewer_name"])
    listing_ids.append(idAppart)
    dates.append(reviewData.loc[i,"date"])
    latLong = findLatLongFromAppartId(idAppart,rawdata)
    latitudes.append(latLong[0])
    longitudes.append(latLong[1])

  data = {
       'reviewer_id' : pd.Series(reviewer_ids),
       'reviewer_name' : pd.Series(reviewer_names),
       'listing_id' : pd.Series(listing_ids),
       'date' : pd.Series(dates),
       'latitude' : pd.Series(latitudes),
       'longitude' : pd.Series(longitudes)}
  dataFrame = pd.DataFrame(data)
  return dataFrame

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# print("================== Position des clients ayant loué en 2018 parmis les 30 premiers clients ==================")
# print(positionClient(reviewData.head(30),rawdata,2018,1))

# ==============================================================================
# listTowns= ['paris','antwerp','barcelona','brussels','geneva','ghent','lyon','vaud','zurich']
listTowns= ['paris']#,'barcelona','antwerp','brussels','geneva','ghent','lyon','vaud','zurich'] # pas 'bordeaux' dedans car je le lis deja avant (dataframe de depart)
gdrive_path = gdrive_path+"/"
revCsv = "/reviews.csv"
listCsv = "/listings.csv"
reviewDataFull = pd.read_csv(gdrive_path+'bordeaux'+revCsv)
listDataFull = pd.read_csv(gdrive_path+'bordeaux'+listCsv)
print("nb row (before):"+str(len(reviewDataFull.index)))
for town in listTowns:
    review_input_file = gdrive_path + town + revCsv
    list_input_file = gdrive_path + town + listCsv
    rdCurrent = pd.read_csv(review_input_file)
    print("    "+town+" nb rows: "+str(len(rdCurrent.index)))
    listCurrent = pd.read_csv(list_input_file)
    reviewDataFull = reviewDataFull.append(rdCurrent, ignore_index=True, sort=False)
    listDataFull = listDataFull.append(listCurrent, ignore_index=True, sort=False)
    print("    new total rows: "+str(len(reviewDataFull.index))+"\n")

print("nb row (after):"+str(len(reviewDataFull.index)))
print("nb row with duplicate index:"+str(len(reviewDataFull[reviewDataFull.index.duplicated()].index)))

def selectClientPresentAtLeastNTimes(reviewDataFull,n):
  counts = reviewDataFull['reviewer_id'].value_counts()
  reviewDataFull=reviewDataFull[reviewDataFull['reviewer_id'].isin(counts.index[counts >= n])]
  return reviewDataFull

# print("nb row :"+str(len(reviewDataFull.index)))
# reviewDataFull = selectClientPresentAtLeastNTimes(reviewDataFull,9)
# print(reviewDataFull.head(30))
# print("nb row :"+str(len(reviewDataFull.index)))

# ======================== Methode simple en utilisant pandas ========================
def positionClientBis(reviewData,listData): 
  listDataRenameAndFilter=listData.rename(columns={"id": "listing_id"}).filter(items=['listing_id','latitude','longitude']) #'neighbourhood_cleansed',
  reviewDataFilter=reviewData.filter(items=['listing_id','reviewer_id','reviewer_name','date'])
  df=reviewDataFilter.join(listDataRenameAndFilter.set_index('listing_id'), on='listing_id').sort_values(by=['reviewer_id','date'])
  df=df[df['latitude'].notna()][df['longitude'].notna()]
  return df

# print("================== Position des clients ayant loué au moins 9 fois chez Airbnb ==================")
# reviewDataFullNTimes = selectClientPresentAtLeastNTimes(reviewDataFull,9)
# print(positionClientBis(reviewDataFullNTimes,listDataFull))

def allPositionOfOneClient(idClient,reviewDataFull,listDataFull):
  reviewDataFull = reviewDataFull[reviewDataFull['reviewer_id'].isin([idClient])] # ca marche
  return positionClientBis(reviewDataFull,listDataFull)

# print("================== Position de Malory (presente au moins 9 fois)==================")
# reviewDataFullNTimes = selectClientPresentAtLeastNTimes(reviewDataFull,9)
# onePersPos = allPositionOfOneClient(51189707,reviewDataFull,listDataFull)# id de Malory
# print(onePersPos) 

def selectNClientsWithTheMostNumberOfOccurences(reviewDataFull,listDataFull,n):
  reviewerList = reviewDataFull['reviewer_id'].value_counts()[:n].index.tolist()
  reviewDataFull = reviewDataFull[reviewDataFull['reviewer_id'].isin(reviewerList)] # ca marche
  return positionClientBis(reviewDataFull,listDataFull)

# posNClientsMostOcc = selectNClientsWithTheMostNumberOfOccurences(reviewDataFull,listDataFull,1)
# print(posNClientsMostOcc)

def afficherTrajectoire(posClients):
  world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
  # world.head()
  dfPos = posClients
  gdfPos = gpd.GeoDataFrame(
      dfPos, geometry=gpd.points_from_xy(dfPos.longitude, dfPos.latitude))

  #zip the coordinates into a point object and convert to a GeoData Frame
  geometry = [Point(xy) for xy in zip(dfPos.longitude, dfPos.latitude)]
  geo_df = gpd.GeoDataFrame(dfPos, geometry=geometry)

  geo_df = geo_df.groupby(['reviewer_id'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist())
  geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry')
  axGeo = geo_df.plot(color='red', zorder=2)

  ax = gdfPos.plot(ax=axGeo,color='k', zorder=3)
  world.plot(ax=ax, zorder=1)
  plt.show()

# afficherTrajectoire(onePersPos)
# afficherTrajectoire(positionClientBis(reviewDataFullNTimes,listDataFull))
# afficherTrajectoire(posNClientsMostOcc)

def concatHisto(town,gdrive_path):
  listDates= ['Dec2020','Jan2021','Feb2021','Mar2021','Apr2021','Jun2021','Jul2021','Aug2021']
  gdrive_path = gdrive_path
  listCsv = "/listings.csv"
  listDataHistoFull = pd.read_csv(gdrive_path+town+listCsv) #premier csv de base (je crois de septembre)
  print("nb row (before):"+str(len(listDataHistoFull.index)))
  for date in listDates:
      list_input_file = gdrive_path + town + '/historique/listings' + date+'.csv'
      listCurrent = pd.read_csv(list_input_file)
      print("    "+town+" nb rows: "+str(len(listCurrent.index)))
      listDataHistoFull = listDataHistoFull.append(listCurrent, ignore_index=True, sort=False)
      print("    new total rows: "+str(len(listDataHistoFull.index))+"\n")

  print("nb row (after):"+str(len(listDataHistoFull.index)))
  print("nb row with duplicate index:"+str(len(listDataHistoFull[listDataHistoFull.index.duplicated()].index)))
  return listDataHistoFull.filter(items=['id','last_scraped','neighbourhood_cleansed','latitude','longitude'])

def selectAppartsAlwaysPresent(reviewDataFull,listDataHistoFull):
  n=9 # 9 car 9 csv (8 dans l'historique et 1 de septembre)
  appartList = listDataHistoFull['id'].value_counts()[:n].index.tolist()
  listDataHistoFull = listDataHistoFull[listDataHistoFull['id'].isin(appartList)]
  return listDataHistoFull

# listDataHistoBordeauFull = concatHisto('bordeaux',gdrive_path)
# print(selectAppartsAlwaysPresent(reviewDataFull,listDataHistoBordeauFull))
# En regardant les positions on voit qu'elles varient mais pas tout le temps
# Sur les 9 fois varient 3 fois sur le 1er id mais le 2eme ne varient pas

def calculMoyennePosId(listDataHistoFull):
  # listDataHistoFull['AvgLat'] = listDataHistoFull.groupby('id')['latitude'].transform('mean')
  # listDataHistoFull['AvgLong'] = listDataHistoFull.groupby('id')['longitude'].transform('mean')
  
  print("================== drop dupli ====================")
  print("nb rows before drop : "+str(len(listDataHistoFull.index)))
  listDataHistoFull=listDataHistoFull.drop_duplicates(subset=['id','latitude','longitude'])
  print("nb rows after drop : "+str(len(listDataHistoFull.index)))
  listDataHistoFull=listDataHistoFull.groupby('id').mean().reset_index()
  return listDataHistoFull

# print(calculMoyennePosId(selectAppartsAlwaysPresent(reviewDataFull,listDataHistoBordeauFull)))


def selectNClients_withTheMostNumberOfOccurences_AvgPos_inTown(town,nbClients,gdrive_path):
  listDataHistoFull = concatHisto(town,gdrive_path)
  listDataHistoMoyFull = calculMoyennePosId(listDataHistoFull)
  # select n clients avec le plus d'occurences
  reviewDataFull = pd.read_csv(gdrive_path+town+"/reviews.csv")
  return selectNClientsWithTheMostNumberOfOccurences(reviewDataFull,listDataHistoMoyFull,nbClients)


# avgPosNClientsMostOcc = selectNClients_withTheMostNumberOfOccurences_AvgPos_inTown('Paris',1,gdrive_path)
# print("================== Position moyenne client le plus présent à Paris ==================")
# print(avgPosNClientsMostOcc)

# afficherTrajectoire(avgPosNClientsMostOcc)

def appartWithPossibilitiesToGetAPositionMorePrecise(town,gdrive_path):
  listDataHistoFull = concatHisto(town,gdrive_path)
  listDataHistoFull=listDataHistoFull.drop_duplicates(subset=['id','latitude','longitude'], keep='first')
  nbAppart = len(listDataHistoFull.drop_duplicates(subset=['id'], keep='first'))
  # listDataHistoFull=listDataHistoFull.groupby('id').filter(lambda x: len(x) >= 2).reset_index() # à la base
  listDataHistoFull['nb_pos_diff']=listDataHistoFull.groupby('id')['id'].transform('count')
  # listDataHistoFull=listDataHistoFull.groupby('id').filter(lambda x: len(x) > 1).drop_duplicates(subset=['id'], keep='first').sort_values(by=['nb_pos_diff'],ascending=False).reset_index()
  listDataHistoFull=listDataHistoFull.groupby('id').filter(lambda x: len(x) > 1)
  listDataHistoFull= listDataHistoFull.groupby('id').mean().sort_values(by=['nb_pos_diff'],ascending=False).reset_index()
  return listDataHistoFull, nbAppart

# town='paris'
# appartMorePrecise, nbAppartBase = appartWithPossibilitiesToGetAPositionMorePrecise(town,gdrive_path)
# print("================== Liste des appartements à "+town+" où il est possible d'avoir des positions plus précises ==================")
# print(appartMorePrecise.head(30))
# print("[ ... ]")
# print("nb d'appartements concernés à "+town+" :"+str(len(appartMorePrecise.index))+" sur les "+str(nbAppartBase)+" appartements.")
# print("cela représente "+str(len(appartMorePrecise.index)/nbAppartBase*100)+"% \des appartements")

# town='bordeaux'
# appartMorePrecise, nbAppartBase = appartWithPossibilitiesToGetAPositionMorePrecise(town,gdrive_path)
# print("================== Liste des appartements à "+town+" où il est possible d'avoir des positions plus précises ==================")
# print(appartMorePrecise.head(30))
# print("[ ... ]")
# print("nb d'appartements concernés à "+town+" :"+str(len(appartMorePrecise.index))+" sur les "+str(nbAppartBase)+" appartements.")
# print("cela représente "+str(len(appartMorePrecise.index)/nbAppartBase*100)+"% \des appartements")


def getPosAppartAndHisMoy_withMostNumberOfOccurences(town,gdrive_path):
  fullHisto = concatHisto(town,gdrive_path)
  listDataHistoFull=fullHisto.drop_duplicates(subset=['id','latitude','longitude'], keep='first')
  listDataHistoFull['nb_pos_diff']=listDataHistoFull.groupby('id')['id'].transform('count')
  listDataHistoFull=listDataHistoFull.groupby('id').filter(lambda x: len(x) > 1)
  listDataHistoFull= listDataHistoFull.groupby('id').mean().sort_values(by=['nb_pos_diff'],ascending=False).reset_index()

  fullHisto = fullHisto.drop_duplicates(subset=['id','latitude','longitude'], keep='first')
  appart = listDataHistoFull.head(1) #index.tolist()
  return fullHisto[fullHisto['id'].isin(appart['id'])], appart

town='paris'
appartPos, appartPosMoy = getPosAppartAndHisMoy_withMostNumberOfOccurences(town,gdrive_path)
print("================== Liste des positions de l'appartement à "+town+" avec le plus grand nombre de positions différentes ==================")
print(appartPos)
print("========> Sa position la plus précise : ")
print(appartPosMoy)

# town='bordeaux'
# appartPos, appartPosMoy = getPosAppartAndHisMoy_withMostNumberOfOccurences(town,gdrive_path)
# print("================== Liste des positions de l'appartement à "+town+" avec le plus grand nombre de positions différentes ==================")
# print(appartPos)
# print("========> Sa position la plus précise : ")
# print(appartPosMoy)

def afficherPosAppart(posApparts,posAppartsMoy):
  world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
  # world.head()
  dfPos = posApparts
  gdfPos = gpd.GeoDataFrame(
      dfPos, geometry=gpd.points_from_xy(dfPos.longitude, dfPos.latitude))

  #zip the coordinates into a point object and convert to a GeoData Frame
  geometry = [Point(xy) for xy in zip(dfPos.longitude, dfPos.latitude)]
  geo_df = gpd.GeoDataFrame(dfPos, geometry=geometry)

  geo_df = geo_df.groupby(['id'])['geometry'].apply(lambda x: Polygon(x.tolist()) if x.size > 1 else x.tolist())
  geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry')

  gdfPosMoy = gpd.GeoDataFrame(
      posAppartsMoy, geometry=gpd.points_from_xy(posAppartsMoy.longitude, posAppartsMoy.latitude))
  axMoy = gdfPosMoy.plot(color='g', zorder=4)

  axGeo = geo_df.plot(ax=axMoy,color='red', zorder=2)
  ax = gdfPos.plot(ax=axGeo,color='k', zorder=3)

  world.plot(ax=ax, zorder=1)
  plt.show()

# afficherPosAppart(appartPos,appartPosMoy)

def mapAppartPosition(posApparts,posAppartsMoy):
  # fig=Figure(height=1000,width=1000)
  map = Map(location=[48.856614, 2.3522219], zoom_start=8, ) # coord Paris
  coords=[]
  firstIndex=-1
  for i in posApparts.index: # car les index ne sont pas un range de 0 à X (1,2,3,...,X)
    if(firstIndex==-1):
      firstIndex=i
    lat = posApparts.loc[i,"latitude"]
    long = posApparts.loc[i,"longitude"]
    coords.append([lat,long])
    Marker(location=[lat,long],popup='['+str(lat)+','+str(long)+']',
      icon=folium.Icon(color='red',icon='none')).add_to(map)
  
  coords.append([posApparts.loc[firstIndex,"latitude"],posApparts.loc[firstIndex,"longitude"]])
  folium.vector_layers.PolyLine(coords,color='blue',weight=5).add_to(map)

  for i in posAppartsMoy.index: # car les index ne sont pas un range de 0 à X (1,2,3,...,X)
    lat = posAppartsMoy.loc[i,"latitude"]
    long = posAppartsMoy.loc[i,"longitude"]
    Marker(location=[lat,long],popup='['+str(lat)+','+str(long)+']',
      icon=folium.Icon(color='green',icon='none')).add_to(map)
  # fig.add_to(map)
  map.save("map.html")
  webbrowser.open("map.html")

# mapAppartPosition(appartPos,appartPosMoy)


def mapAfficherTrajectoire(posClients):
  map = Map(location=[48.856614, 2.3522219], zoom_start=6, ) # coord Paris
  coords=[]
  index=0
  for i in posClients.index: # car les index ne sont pas un range de 0 à X (1,2,3,...,X)
    lat = posClients.loc[i,"latitude"]
    long = posClients.loc[i,"longitude"]
    coords.append([lat,long])
    if(index==0):
      Marker(location=[lat,long],popup='index: '+str(index)+' ; ['+str(lat)+','+str(long)+']',
        icon=folium.Icon(color='green',icon='none'),z_index_offset=1).add_to(map)
    else:
      Marker(location=[lat,long],popup='index: '+str(index)+' ; ['+str(lat)+','+str(long)+']',
        icon=folium.Icon(color='red',icon='none')).add_to(map)
    index=index+1
  
  folium.vector_layers.PolyLine(coords,color='blue',weight=5).add_to(map)
  map.save("mapTraj.html")
  webbrowser.open("mapTraj.html")

posNClientsMostOcc = selectNClientsWithTheMostNumberOfOccurences(reviewDataFull,listDataFull,1)
mapAfficherTrajectoire(posNClientsMostOcc)