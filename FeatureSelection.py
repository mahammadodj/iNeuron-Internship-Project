import pandas as pd
import numpy as np
from FeatureEngineering import data

# remove 'weather_description', 'year' column
data.drop(['weather_description','year'], axis=1, inplace=True)
data.drop(['snow_1h','rain_1h'],inplace=True,axis=1)

data.set_index('date_time',inplace=True)

X = data.drop('traffic_volume', axis=1)
y = data['traffic_volume']