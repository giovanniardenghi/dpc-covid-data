import pandas as pd
import numpy as np

data = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
data_Italia = data.groupby('data_somministrazione').sum()
 
new_max = max(data_Italia.index) + pd.Timedelta(35,'days')
new_index = pd.date_range('2020-02-24',new_max)

data_Italia = data_Italia.reindex(new_index,columns=['prima_dose','seconda_dose']).ffill()

regions = [x for _, x in data.groupby(['data_somministrazione','area'])]
for x in regions:
    data_reg = x.reindex(new_index,columns=['prima_dose','seconda_dose']).ffill()
    x.to_csv('data/vaccini_regioni/'+x.area.values[0]+'.csv',index=None)
    
data_Italia.to_csv('data/vaccines.csv',index_label='data')
