#Author: TropoSco#
#Date: 27-08-2014#
#Bike share Qucit challenge#
#Python version: 2.7.8



####Uploading data####

import os
import pandas as pd
import csv


os.chdir("c:\\users\\ALOUINI Yassine\\Documents\\GitHub\\bikeshare-challenge\\bikeshare-challenge\\submissions\\TropoScoSolution")#Changing directory to where the data is located




bikeStationsData = pd.read_csv("stations.csv", index_col=["station_id"],  usecols=["station_id","name", "total_slots"])# The stations data (number of bike slots for different stations)


#From bikeStationData we can retrieve the station_id of each station and the slots available for each one



#Notice that by changing the usecols in the stations.csv file, one can also perform data vizualization for the stations in Bordeaux map


histData= pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure"], usecols=["date", "heure","station_id","status", "bikes", "slots"])

#histData is a  3 months long data base (time step of 1hour), should be split into a training and testing sets (splitting in the Machine Learning and Prediction section)


currentBikes = pd.read_csv("snapshots-actuelle.csv", index_col=["station_id"], usecols=["station_id","bikes"])#When we say current, which time step does it represent ?



####Machine Learning and Prediction####


import sklearn as skl #Importing sci-kit learn package for the ML

###Try Random Forests###


####Data Viz (to be done later)####


###The data###

bikeStationsDataViz = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots", "latitude","longitude"])

###Viz package###

from GeoBases import GeoBase #The GeoBases library doesn't yet work, investigate later


#To be continued of course