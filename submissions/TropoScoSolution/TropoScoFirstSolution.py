#Author: TropoSco#
#Date: 27-08-2014#
#Bike share Qucit challenge#
#Python version: 2.7.8



#Uploading data

import os
import pandas as pd
from StringIO import StringIO
import csv


os.chdir("c:\\users\\ALOUINI Yassine\\Documents\\GitHub\\bikeshare-challenge\\bikeshare-challenge\\submissions\\TropoScoSolution")#Changing directory to where the data is located




bikeStationsData = pd.read_csv("stations.csv", index_col=["station_id"])# The stations data (number of bike slots for different stations)


#Data Viz for the bike stations data (to be done in the near future)




