import pandas
import io
import pandas as pd
import numpy as np
import time
import os
import datetime
import matplotlib.pyplot as plt
import statsmodels
import statsmodels.api as sm
from __future__ import division
import math
from datetime import timedelta


DATA_PATH = '/Users/chenlong/projet/occupation/snapshots-bdx.csv-2.bz2'
WEATHER_PATH = '/Users/chenlong/projet/occupation/weather/weather.csv'

def model_1(timeseries, tau):
    """
        Input :
        timeseries : observed quantity we want to predict
        tau : time interval
        
        Return :
        numpy.ndarray who containing number of predicted bikes using model 1
        
        Supplement :
        t : step of time
        Model 1 : A_predicted(t+tau) = A_observed(t)
        """
    predicted = []
    for t in range(tau):
        # we put -1 when predicted value is undefined
        predicted.append(-1)
    for t in range(tau, len(timeseries)):
        predicted.append( timeseries[t-tau] )
    return np.array(predicted)

def increment(timeseries,tau):
    increment = []
    for i in range(1,tau+1):
        increment.append(model_1(timeseries,i-1)-model_1(timeseries,i))
    return increment



data = pd.read_csv(DATA_PATH, \
	sep=';',encoding='latin1', parse_dates=["date"],compression='bz2', dayfirst=True, index_col="date")
data_weather = pd.read_csv(WEATHER_PATH,sep=';')


""" creat a variable date_time as index and order data by index """
date_time=[]
for i in range(len(data_weather)):
    date_time.append((datetime.datetime.strptime(str(data_weather['date'][i]),"%Y-%m-%d"))+timedelta(hours=data_weather['local_hour'][i]))
data_weather.index = date_time
data_weather = data_weather.sort_index()
data_weather_comp = data_weather.asfreq('1h',method = 'pad')


""" create a data_pluie_incr containing varaible weather(pluie,temperature...), increment, id_station and hour for all stations"""
### we have theses variables og weather : visibility_in_km, temperature_in_celsius, humidity_in_pct, \
### humidex, windchill_in_celsius,wind_in_kmh,pressure_in_hpa

t1 = time.clock()
increment_station = []
pluie_station=[]
hour_station=[]
id_station = []
all_increment = pd.DataFrame()
all_pluie = pd.DataFrame()
all_hour = pd.DataFrame()
data_pluie_incr = pd.DataFrame()
all_id_station = pd.DataFrame()
for j in range(1,140):
    data_one_station = data[data['station_id']==j].asfreq('1h' , method = 'pad')
    data_one_station['hour'] = data_one_station.index.map(lambda x: x.hour)
    hour_station.append(data_one_station['hour'])
    data_one_station['increment'] = increment(data_one_station['bikes'],1)[0]
    increment_station.append(data_one_station['increment'])  
    """ change precipitation_in_mmh to other variable of weather to look his relation with increment or increment_mean """ 
    # we add .map(lambda x: round(x)) before tolist() if we use others variables (so we use just values integers)
    data_one_station['pluie']=data_weather_comp['precipitation_in_mmh'].tolist()[:len(data_one_station)]
    pluie_station.append(data_one_station['pluie']) 
    id_station.append(data_one_station['station_id'])
all_increment = pd.concat(increment_station,axis=0,ignore_index=False).map(lambda x: abs(x))
all_pluie = pd.concat(pluie_station,axis=0,ignore_index=False)
all_hour = pd.concat(hour_station,axis=0,ignore_index=False)
all_id_station = pd.concat(id_station,axis=0,ignore_index=False)
data_pluie_incr = pd.concat([all_pluie,all_hour,all_increment,all_id_station],axis=1,ignore_index=False)
print data_pluie_incr
t2 = time.clock()
print t2-t1


data_pluie_incr.groupby('pluie').mean()
data_pluie_incr.groupby('pluie').mean()['increment'].plot()
plt.ylabel('Increment_moyen')
plt.title('incr_moyen_pluie_all_stations')
plt.show()


### compute increment_mean for each value of pluie and each station
mean_by_station_pluie = data_pluie_incr.groupby(['station_id','pluie']).mean()


### desine graphes with the points reals and fittedvalues from regression
total_stations = 140
for i in range(1,total_stations+1):
    data_mean_by_station = mean_by_station_pluie.query('station_id=='+str(i))
    I_mean_by_station=data_mean_by_station['increment']
    P_by_station=I_mean_by_station.index.get_level_values('pluie').tolist() 
    model=sm.OLS(I_mean_by_station,sm.add_constant(P_by_station))
    fit=model.fit()
    fittedvalues=fit.fittedvalues
    plt.figure()
    plt.plot(P_by_station,I_mean_by_station,'*',label="data")
    plt.plot(P_by_station,fittedvalues,'-',label="Linear_Regression")
    plt.xlim([-0.2,max(P_by_station)+0.2])
    plt.ylim([min(min(fittedvalues),min(I_mean_by_station))-0.1,max(max(fittedvalues),max(I_mean_by_station))+0.1])
    plt.xlabel('precipitation_in_mmh')
    plt.ylabel('Increment_moyen')
    plt.legend( loc='best', numpoints = 1 )
    plt.savefig('/Users/chenlong/projet/graphes/graphes for increment_moyen/LR_Incr_mean_pluie/LR_station_' + str(i) +'.png')






