import anvil.server
import time
from urllib.request import urlopen
import pandas as pd
import pickle
import warnings

warnings.filterwarnings('ignore')

def app_func():

    anvil.server.connect('XFYQ3CHMJT4KDIKHK5L3L6U2-Z3Q5PLFWEGEDIH4Y')

    @anvil.server.callable

    def pred(weekday, month, holiday, hour, weather_main, clouds_all, temp):
        
        path = urlopen(r'https://github.com/MuhammadOo/iNeuron-Internship-Project/raw/master/mypickle.pkl')
        
        cols = ['holiday','temp','clouds_all','weather_main','weekday','hour','month']
        
        pipeline=pickle.load(path)
        
        x = [0 for i in range(1,8)]
        x[0] = holiday
        x[1] = temp
        x[2] = clouds_all
        x[3] = weather_main
        x[4] = weekday
        x[5] = hour
        x[6] = month
        
        
        test_row = pd.DataFrame(x).transpose()
        test_row.columns = cols
        result = pipeline.predict(test_row)
        time.sleep(2)
        
        return round(result[0],0)
    
    anvil.server.wait_forever()

