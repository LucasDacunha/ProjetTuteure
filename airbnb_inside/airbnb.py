import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from google.colab import drive
drive.mount._DEBUG = True
# print(getpass.getpass())
drive.mount('/content/drive')

my_path = "/AirbnbInside" # THIS is your GDrive path
gdrive_path = "/content/drive" + "/My Drive" + my_path
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


dfListe = decoupeZone(rawdata.filter(items=['id','last_scraped','neighbourhood_cleansed','latitude','longitude']))
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
nbAppartParQuartier = appartParQuartier(dfListe)
# le graph ne marche plus pour une raison inconnue je n'ai pas modifier le code
# fig, ax = plt.subplots(figsize=(10,15))
# ax.barh(dfListe[1], nbAppartParQuartier)
# plt.show()

review_input_file = gdrive_path + "/bordeaux/reviews.csv"
reviewData = pd.read_csv(review_input_file)

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
print("================== Position des clients ayant loué en 2018 parmis les 30 premiers clients ==================")
print(positionClient(reviewData.head(30),rawdata,2018,1))

# ==============================================================================
listTowns= ['paris'] # pas 'bordeaux' dedans car je le lis deja avant (dataframe de depart)
gdrive_path = gdrive_path+"/"
revCsv = "/reviews.csv"
listCsv = "/listings.csv"
reviewDataFull = pd.read_csv(gdrive_path+'bordeaux'+revCsv)
listDataFull = pd.read_csv(gdrive_path+'bordeaux'+listCsv)
for town in listTowns:
  review_input_file = gdrive_path + town + revCsv
  list_input_file = gdrive_path + town + listCsv
  rdCurrent = pd.read_csv(review_input_file)
  listCurrent = pd.read_csv(list_input_file)
  reviewDataFull.append(rdCurrent)
  listDataFull.append(listCurrent)

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
  return df

print("================== Position des clients ayant loué au moins 9 fois chez Airbnb ==================")
reviewDataFullNTimes = selectClientPresentAtLeastNTimes(reviewDataFull,9)
print(positionClientBis(reviewDataFullNTimes,listDataFull))

def allPositionOfOneClient(idClient,reviewDataFull,listDataFull):
  reviewDataFull = reviewDataFull[reviewDataFull['reviewer_id'].isin([idClient])] # ca marche
  return positionClientBis(reviewDataFull,listDataFull)

print("================== Position de Malory (presente au moins 9 fois)==================")
reviewDataFullNTimes = selectClientPresentAtLeastNTimes(reviewDataFull,9)
print(allPositionOfOneClient(51189707,reviewDataFull,listDataFull)) # id de Malory
