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
from matplotlib.mlab import PCA as Pca
from pylab import *
from matplotlib.ticker import FormatStrFormatter


DATA_PATH = '/Users/chenlong/projet/occupation/snapshots-bdx.csv-2.bz2'
WEATHER_PATH = '/Users/chenlong/projet/occupation/weather/weather.csv'


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

""" PCA """
#'visibility_in_km','temperature_in_celsius','humidity_in_pct','humidex','windchill_in_celsius','wind_in_kmh', 'pressure_in_hpa','precipitation_in_mmh'
data_weather_variables = data_weather_comp[['temperature_in_celsius','humidity_in_pct']]
array_weather_variables = np.array(data_weather_variables)


results = Pca(array_weather_variables)
Inertie_pourcentage = results.fracs
vectors_propres = results.Wt
principal_componants = results.Y
matrix_centree_resuite = results.a


PC = results.Y
PC1 = results.Y[:,0] # = (visibility_in_km-mean(visibility_in_km))/std(visibility_in_km) * vectors_propres[0,0]
                     # + (temperature_in_celsius-mean(temperature_in_celsius))/std(temperature_in_celsius) * vectors_propres[0,1]
                     # + ... + (precipitation_in_mmh-mean(precipitation_in_mmh))/std(precipitation_in_mmh) * vectors_propres[0,7]
PC2 = results.Y[:,1]

""" graphs pf the points sur PC1 and PC2 """
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(PC1,PC2)

ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')



""" graphs of the points originals with PC1 and PC2 """
plt.figure()
m = np.mean(array_weather_variables,axis=0)
std = np.std(array_weather_variables,axis=0)
plt.plot([-vectors_propres[0,1]*20*std[0], vectors_propres[0,1]*20*std[0]]+m[0], [-vectors_propres[1,1]*20*std[1], vectors_propres[1,1]*20*std[1]]+m[1],'r-')
plt.plot([-vectors_propres[0,0]*20*std[0], vectors_propres[0,0]*20*std[0]]+m[0], [-vectors_propres[1,0]*20*std[1], vectors_propres[1,0]*20*std[1]]+m[1],'r-')
plt.xlim([-5,25])
plt.ylim([0,120])
plt.plot(array_weather_variables[:,0],array_weather_variables[:,1],'.')# the data
plt.show()


