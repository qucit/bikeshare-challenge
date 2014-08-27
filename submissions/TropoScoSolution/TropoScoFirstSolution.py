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


#Notice that by changing the usecols in the stations.csv file, one can also perform data vizualization for the stations in Bordeaux map


snapshots = pd.read_csv("snapshots-bdx.csv",  index_col=["station_id","heure"], usecols=["date", "heure","station_id","status", "bikes", "slots"])#change this variable name


currentBikes = pd.read_csv("snapshots-actuelle.csv", index_col=["station_id"], usecols=["station_id","bikes"])#change the$is variable name




####Data Viz####


bikeStationsDataViz = pd.read_csv("stations.csv", index_col=["station_id"], usecols=["station_id","name", "total_slots", "latitude","longitude"])



#To be continued of course