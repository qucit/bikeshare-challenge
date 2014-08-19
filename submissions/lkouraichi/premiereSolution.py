
import pandas as pd
import math

# premiere solution si le nombre des bicyclettes n est pas connu pour trouver la prediction dans deux heures

# Recuperer la liste des stations ainsi les informations reliees a partir du fichier station.csv
#utiliser la librairie PANDAS pour le parsing 
stations = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots"])

#recuperer le flux de mouvement a partir snapshots-bdx.csv
#utiliser la librairie PANDAS pour le parsing 
snapshots = pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure", "date"], usecols=["date", "heure","station_id","status", "bikes", "slots"])

#on va faire le calcul du prediction pour chaque station, alors on doit regrouper le flux(snapshots) en fonction l identifiant de station. (c est plus perfermant que le parcour du flux), toujour en utilsant la libraire PANDAS
snapshotGrouped = snapshots.groupby(level=['station_id'])

# La fonction convertirEnEntier peremt de faire la tendence d'une valeure reel vers une valeur entiere 
# convertirEnEntier(2.4)= 2   convertirEnEntier(2.6)=3
def convertirEnEntier(valeureReelle):
  return int(valeureReelle + 0.5)

# TO DO, passer l heure en parametre, pour le moment, je teste avec 00:00:00 (statique)
#Nous avons regroupees le flux en un ensemble des groupes. Chaque groupe presente le flux pour chaque station. 
#cette fonction s applique a chaque groupe pour calculer le nombre des bicyclettes (trouver une prediction).
#Dans cette solution, on va calculer la moyenne 
def calculerNombreBicyclettesParStation(snapshotStation):
  #le flux contient toutes les valeurs pour des differentes heures et dates.
  #on va faire une selection pour une heure precise (heure de la prediction).
  #nous aurons comme resultat le nombre des bicyclettes pour tous les jours a l heure 00:00:00 (un tableau avec une seule colonne "bikes")
  dataFrameBikes = snapshotStation.reset_index().set_index(['heure']).ix["00:00:00"]['bikes']
  #toujours en utilisant PANDAS on va calculer la moyenne et on va retouner la valeur entiere
  return convertirEnEntier(dataFrameBikes.mean())
 
#appliquer la fonction calculerNombreBicyclettesParStation pour calculer le nombre des bicyclettes pour cahque station
df=snapshotGrouped.apply(calculerNombreBicyclettesParStation)

#Faire une jointure pour afficher le nom du station avec sa prediction trouvee dans deux heures
resultat = pd.concat([stations, df], axis=1)


print resultat




