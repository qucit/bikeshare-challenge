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
from matplotlib.ticker import FormatStrFormatter

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
    """
       increment of bikes for a time step tau
    """
    increment = []
    for i in range(1,tau+1):
        increment.append(model_1(timeseries,i-1)-model_1(timeseries,i))
    return increment


""" import data"""

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



""" If you want to change the variable, there are 2 parts to change, One is histogramme, another is for creat data_pluie_incr """


"""histogramme """
"""add .map(lambda x: round(x)) for variables not precipitation_in_mmh (before .dropna())"""

pluie=data_weather_comp['precipitation_in_mmh'].dropna()
unique_pluie=np.unique(pluie)
plt.hist(pluie,unique_pluie)
plt.show()

""" an histogramme beautiful and clear"""
bins_choose = 30 ## il faut bien choisir bins for differents variables, we propose bins=30
fig, ax = plt.subplots()
counts, bins, patches = ax.hist(pluie,bins = bins_choose, facecolor='yellow', edgecolor='gray')

ax.set_xticks(bins)
ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))


twentyfifth, seventyfifth = np.percentile(pluie, [25, 75])
for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
    if rightside < twentyfifth:
        patch.set_facecolor('green')
    elif leftside > seventyfifth:
        patch.set_facecolor('red')


bin_centers = 0.5 * np.diff(bins) + bins[:-1]
for count, x in zip(counts, bin_centers):
    # Label the raw counts
    ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
        xytext=(0, -18), textcoords='offset points', va='top', ha='center')

    # Label the percentages
    percent = '%0.0f%%' % (100 * float(count) / counts.sum())
    ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
        xytext=(0, -32), textcoords='offset points', va='top', ha='center')
plt.show()



""" create a data_pluie_incr containing varaible weather(pluie,temperature...), increment, id_station and hour for all stations"""
### we have theses variables og weather : precipitation_in_mmh,visibility_in_km, temperature_in_celsius, humidity_in_pct, \
### humidex, windchill_in_celsius,wind_in_kmh,pressure_in_hpa, gust_in_kmh

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
    """we add .map(lambda x: round(x)) before tolist() if we use others variables (so we use just values integers)"""
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


""" graphe of increment_mean of all stations """
data_pluie_incr.groupby('pluie').mean()
data_pluie_incr.groupby('pluie').mean()['increment'].plot()
plt.ylabel('Increment_moyen_abs')
plt.xlabel('precipitation_in_mmh')
plt.title('incr_moyen_pluie_all_stations')

plt.show()


### compute increment_mean for each value of pluie and each station
mean_by_station_pluie = data_pluie_incr.groupby(['station_id','pluie']).mean()


### desine graphes with the points reals and fittedvalues from regression
total_stations = 1
for i in range(1,total_stations+1):
    data_mean_by_station = mean_by_station_pluie.query('station_id=='+str(i))
    I_mean_by_station=data_mean_by_station['increment']
    P_by_station=I_mean_by_station.index.get_level_values('pluie')
    model=sm.OLS(I_mean_by_station,sm.add_constant(P_by_station))
    fit=model.fit()
    fittedvalues=fit.fittedvalues
    plt.figure()
    plt.plot(P_by_station,I_mean_by_station,'*',label="data")
    plt.plot(P_by_station,fittedvalues,'-',label="Linear_Regression")
    plt.xlim([min(P_by_station)-0.2,max(P_by_station)+0.2])
    plt.ylim([min(min(fittedvalues),min(I_mean_by_station))-0.1,max(max(fittedvalues),max(I_mean_by_station))+0.1])
    plt.xlabel('precipitation_in_mmh')
    plt.ylabel('Increment_moyen_abs')
    plt.legend( loc='best', numpoints = 1 )
    plt.savefig('/Users/chenlong/projet/graphes/graphes for increment_moyen/LR_Incr_mean_pluie/LR_station_' + str(i) +'.png')



""" for variable wind and gust """
total_stations = 139
for i in range(1,total_stations+1):
    data_mean_by_station = mean_by_station_pluie.query('station_id=='+str(i))
    I_mean_by_station=data_mean_by_station['increment']
    P_by_station=I_mean_by_station.index.get_level_values('pluie')
    x=np.column_stack((P_by_station, P_by_station**2))
    model=sm.OLS(I_mean_by_station,sm.add_constant(x))
    fit=model.fit()
    fittedvalues=fit.fittedvalues
    plt.figure()
    plt.plot(P_by_station,I_mean_by_station,'*',label="data")
    plt.plot(P_by_station,fittedvalues,'-',label="Linear_Regression")
    plt.xlim([min(P_by_station)-0.2,max(P_by_station)+0.2])
    plt.ylim([min(min(fittedvalues),min(I_mean_by_station))-0.1,max(max(fittedvalues),max(I_mean_by_station))+0.1])
    plt.xlabel('wind_in_kmh')
    plt.ylabel('Increment_moyen_abs')
    plt.legend( loc='best', numpoints = 1 )
    plt.savefig('/Users/chenlong/projet/graphes/graphes for increment_moyen/LR_Incr_mean_wind/LR_station_' + str(i) +'.png')





