import pandas as pd
import numpy as np

data = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
data = data.groupby('data_somministrazione').sum()

repeated_values = data.iloc[-7:,1:]
first_forecast = max(data.index) + pd.Timedelta(1,'day')
last_repeated = max(data.index) + pd.Timedelta(22,'day') 
new_max = max(data.index) + pd.Timedelta(35,'days')
new_index = pd.date_range('2020-02-24',new_max)

data = data.reindex(new_index,columns=['prima_dose','seconda_dose']).ffill()


data.to_csv('data/vaccines.csv',index_label='data')
