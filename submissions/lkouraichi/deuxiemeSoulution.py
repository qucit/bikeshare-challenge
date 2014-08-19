
import pandas as pd
import math

# premiere solution si le nombre des bicyclettes n est pas connu pour trouver la prediction dans deux heures

# Recuperer la liste des stations ainsi les informations reliees a partir du fichier station.csv
#utiliser la librairie PANDAS pour le parsing 
stations = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots"])

act = pd.read_csv("snapshots-actuelle.csv", index_col=["station_id"], usecols=["station_id","bikes"])

#recuperer le flux de mouvement a partir snapshots-bdx.csv
#utiliser la librairie PANDAS pour le parsing 
snapshots = pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure"], usecols=["date", "heure","station_id","status", "bikes", "slots"])

#on va faire le calcul du prediction pour chaque station, alors on doit regrouper le flux(snapshots) en fonction l identifiant de station. (c est plus perfermant que le parcour du flux), toujours en utilsant la libraire PANDAS

snapshots2 = snapshots[snapshots.status > 0]

snapshotGrouped = snapshots2.groupby(level=['station_id'])


a= str(10)

def convertirEnEntier(valeureReelle):
  if (valeureReelle>0):
    return int(valeureReelle + 0.5)
  else:
    return int(valeureReelle - 0.5)


def calculerNombreBicyclettesAjouteeDansDeuxHeuresParStation(snapshotStation):
  dataFrameBikesNow = snapshotStation.reset_index().set_index(['heure']).ix["10:00:00"].set_index(['date'])['bikes']
  dataFrameAfterTwoHours = snapshotStation.reset_index().set_index(['heure']).ix["12:00:00"].set_index(['date'])
  df=dataFrameAfterTwoHours.rename(columns = {'bikes':'bikes After 2 hours'})
  dataFrameBikesAfterTwoHours=df['bikes After 2 hours']
  dataFrameBikes = pd.concat([dataFrameBikesNow, dataFrameBikesAfterTwoHours], axis=1, join='inner')
  df2 = dataFrameBikes['bikes After 2 hours'] - dataFrameBikes['bikes']
  return convertirEnEntier(df2.mean())
 

df=snapshotGrouped.apply(calculerNombreBicyclettesAjouteeDansDeuxHeuresParStation)

print df.sum()

df7 = pd.concat([df, act], axis=1, join='inner')
#print df7
df7 = df7[0] + df7['bikes']
#print df7

resultat = pd.concat([stations, df], axis=1)


#print resultat





