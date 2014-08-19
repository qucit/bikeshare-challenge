# deuxieme solution : nombre de velo par station connu et recuperee a partir d un fichier

import pandas as pd
import math
 
# Recuperer la liste des stations ainsi les informations relieesa partir du fichier station.csv
stations = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots"])

# Recuperer les occupations a partir snapshots-bdx.csv
snapshots = pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure"], usecols=["date", "heure","station_id","status", "bikes", "slots"])

# Recuperer les occupations actuelle pour chaque station
currentBikes = pd.read_csv("snapshots-actuelle.csv", index_col=["station_id"], usecols=["station_id","bikes"])

#calcul du prediction pour chaque station => regrouper les occupations(snapshots) en fonction l identifiant de station. (c est plus perfermant que le parcour du flux), toujours en utilsant la libraire PANDAS

snapshots2 = snapshots[snapshots.status > 0]

snapshotGrouped = snapshots2.groupby(level=['station_id'])


# TO DO mettre l'heure en parametre

# calcul de l increment moyen par station dans deux heures
def meanincrementperstation(snapshotStation):
  BikesNow = snapshotStation.reset_index().set_index(['heure']).ix["10:00:00"].set_index(['date'])['bikes']
  AfterTwoHours = snapshotStation.reset_index().set_index(['heure']).ix["12:00:00"].set_index(['date'])
  AfterTwoHours=AfterTwoHours.rename(columns = {'bikes':'bikes After 2 hours'})
  BikesAfterTwoHours=AfterTwoHours['bikes After 2 hours']
  Bikes = pd.concat([BikesNow, BikesAfterTwoHours], axis=1, join='inner')
  df2 = Bikes['bikes After 2 hours'] - Bikes['bikes']
  return int(round(df2.mean()))
 

df=snapshotGrouped.apply(meanincrementperstation)

df = pd.concat([df, currentBikes], axis=1, join='inner')

#Ajout de l increment pour chaque station
df = df[0] + df['bikes']

# Jointure pour afficher la prediction pour chaque station
resultat = pd.concat([stations, df], axis=1)
print resultat





