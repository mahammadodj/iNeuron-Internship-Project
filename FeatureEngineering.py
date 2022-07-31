#importing required libraries
import numpy as np
import pandas as pd

import warnings 
warnings.filterwarnings(action='ignore')

# Exploratory Data Analysis (EDA)

# specifying client_id and client_secret to connect to cassandra database
client_id = "mlIYceFbdjDIIbJoMUAZqlSw"
client_secret = "24OAHYj3OFitt5I,P-rCo5yBgkwwwEDuZrE9FZ9ZEFfuozXIZCL,JH_O_2oRQZiceO19ATi_8-8143cYAR5cnW0AOQ,3ZIDhxSSfw_LKtCLL_SZbmagFYw_WPFMpi-os"

# connecting to cassandra database
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
        'secure_connect_bundle': 'secure-connect-metro-traffic.zip'
}
auth_provider = PlainTextAuthProvider(client_id, client_secret)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

df = pd.DataFrame(list(session.execute("SELECT * FROM traffic_volume.metro")))

df['date_time']=pd.to_datetime(df['date_time'])
df['rain_1h']=df['rain_1h'].astype('float64')
df['snow_1h']=df['snow_1h'].astype('float64')
df['temp']=df['temp'].astype('float64')
df.sort_values(by=['date_time'],inplace=True)
df['temp']=df['temp']-273

# define function to remove outliers
def remove_outlier(df,x):
    Q3,Q1 = np.percentile(df,[75,25])
    IQR = Q3 - Q1
    # Upper bound
    upper = np.where(df >= (Q3+1.5*IQR))
    # Lower bound
    lower = np.where(df <= (Q1-1.5*IQR))
 
    #Removing the Outliers
    x.drop(upper[0], inplace = True)
    x.drop(lower[0], inplace = True)
    
remove_outlier(df['temp'],df)

data = df.copy()
# create new columns from date_time
data['weekday'] = data.date_time.dt.weekday
data['hour'] = data.date_time.dt.hour
data['month'] = data.date_time.dt.month
data['year'] = data.date_time.dt.year

#Monday is 0 and Sunday is 6
def hour_modify(x):
    Early_Morning = [4,5,6,7]
    Morning = [8,9,10,11]
    Afternoon = [12,13,14,15]
    Evening = [16,17,18,19]
    Night = [20,21,22,23]
    Late_Night = [24,1,2,3]
    if x in Early_Morning:
        return 'Early Morning'
    elif x in Morning:
        return 'Morning'
    elif x in Afternoon:
        return 'Afternoon'
    elif x in Evening:
        return 'Evening'
    elif x in Night:
        return 'Night'
    else:
        return 'Late Night'
    
data['hour'] = data.hour.apply(hour_modify)

def modify_holiday(x):
    if x == 'None':
        return False
    else:
        return True
    
data['holiday'] = data['holiday'].apply(modify_holiday)
data[['month','weekday']] = data[['month','weekday']] .astype('category')