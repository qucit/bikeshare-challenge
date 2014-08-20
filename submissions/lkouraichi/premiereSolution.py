# premiere solution le nombre de velos n est pas connu 

import pandas as pd
import math


# Recuperer la liste des stations ainsi les informations reliees a partir du fichier station.csv
stations = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots"])

# Recuperer les occupations a partir snapshots-bdx.csv
snapshots = pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure", "date"], usecols=["date", "heure","station_id","status", "bikes", "slots"])

#on va faire le calcul du prediction pour chaque station, alors on doit regrouper les occupations(snapshots) en fonction l identifiant de station. (c est plus perfermant que le parcour du flux)
snapshotGrouped = snapshots.groupby(level=['station_id'])

# TO DO, passer l heure en parametre, pour le moment, je teste avec 00:00:00 (statique)
# calcul de la moyenne pour chaque heure pour une station
def bikesperstation(snapshotStation):
  dataFrameBikes = snapshotStation.reset_index().set_index(['heure']).ix["00:00:00"]['bikes']
  #calcule de la moyenne
  return int(round(dataFrameBikes.mean()))
 
#appliquer la fonction bikesperstation pour calculer le nombre de velo pour cahque station
df=snapshotGrouped.apply(bikesperstation)

#Faire une jointure pour afficher le nom du station avec sa prediction trouvee dans deux heures
resultat = pd.concat([stations, df], axis=1)


print resultat




