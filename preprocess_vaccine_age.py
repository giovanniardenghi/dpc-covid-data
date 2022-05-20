import pandas as pd
import numpy as np
sigla_regioni = {
    'ITA':'Italia',
    'ABR':'Abruzzo',
    'BAS':'Basilicata',
    'CAL':'Calabria',
    'CAM':'Campania',
    'EMR':'Emilia-Romagna',
    'FVG':'Friuli Venezia Giulia',
    'LAZ':'Lazio',
    'LIG':'Liguria',
    'LOM':'Lombardia',
    'MAR':'Marche',
    'MOL':'Molise',
    'PAB':'P.A. Bolzano',
    'PAT':'P.A. Trento',
    'PIE':'Piemonte',
    'PUG':'Puglia',
    'SAR':'Sardegna',
    'SIC':'Sicilia',
    'TOS':'Toscana',
    'UMB':'Umbria',
    'VDA':'Valle d\'Aosta',
    'VEN':'Veneto'
}

pops = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea.csv')
pops = pops.groupby('area').sum().totale_popolazione
pops['ITA'] = pops.sum()

data = pd.read_csv(
    'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

data=data.rename(columns={"data": "data_somministrazione",
                           "forn":  "fornitore",
                           "area":  "area",
                           "eta":   "fascia_anagrafica",
                           "m":     "sesso_maschile",
                           "f":     "sesso_femminile",
                           "d1":    "prima_dose",
                           "d2":    "seconda_dose",
                           "dpi":   "pregressa_infezione",
                           "db1":   "dose_addizionale_booster",
                           "dbi":   "booster_immuno",
                           "db2":   "d2_booster",
                           "N1":    "codice_NUTS1",
                           "N2":    "codice_NUTS2",
                           "ISTAT": "codice_regione_ISTAT",
                           "reg":   "nome_area"
    })
data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
#data = data[data['data_somministrazione']<='2021-03-25']
monodose = data[data['fornitore']=='Janssen']

#data.drop(monodose.index, inplace=True)
monodose = monodose.groupby(['data_somministrazione','fascia_anagrafica']).sum()
data_Italia =  data.groupby(['data_somministrazione','fascia_anagrafica']).sum()
data_Italia['mono_dose'] = monodose['prima_dose']
data_Italia.fillna(0,inplace=True)

max_Italia_index = max(data_Italia.index)[0]
new_max = max_Italia_index# + pd.Timedelta(100, 'days')
new_index = pd.date_range(min(data_Italia.index)[0], new_max)
new_index = pd.MultiIndex.from_product([new_index, ('12-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90+')])

today = str(pd.Timestamp.today()+pd.Timedelta(2, 'day'))[:10]
#today = '2021-03-26'
print(today)

data_Italia['prima_dose'] = data_Italia.prima_dose-data_Italia.mono_dose
data_Italia['seconda_dose'] = data_Italia.seconda_dose+data_Italia.mono_dose+data_Italia.pregressa_infezione
data_Italia['terza_dose'] = data_Italia.dose_addizionale_booster

print(data_Italia)
#data_Italia.loc[pd.to_datetime(today),['prima_dose','seconda_dose']] = 3e5
#data_Italia.loc[pd.to_datetime(today),['terza_dose']] = 4e5
#data_Italia.loc[max_Italia_index + pd.Timedelta(1, 'day')] = data_Italia.iloc[-7:, :].mean().round()
data_Italia = data_Italia.reindex(new_index, columns=['prima_dose', 'seconda_dose', 'terza_dose', 'pregressa_infezione', 'mono_dose'], fill_value=0)
#data_Italia['prima_dose_tot'] = data_Italia.prima_dose.cumsum()
#data_Italia['seconda_dose_tot'] = data_Italia.seconda_dose.cumsum()
#data_Italia['terza_dose_tot'] = data_Italia.terza_dose.cumsum()
#data_Italia['mono_dose_tot'] = data_Italia.mono_dose.cumsum()
#data_Italia['pregressa_infezione_tot'] = data_Italia.pregressa_infezione.cumsum()
#if np.argmax(data_Italia.prima_dose_tot > pops['ITA']-data_Italia.iloc[:,-2] - data_Italia.iloc[:,-1]):
#    max_idx = np.argmax(data_Italia.prima_dose_tot > pops['ITA']-data_Italia.iloc[:,-2] - data_Italia.iloc[:,-1])
#    data_Italia.iloc[max_idx:, 0] = 0
#    data_Italia.iloc[max_idx:, 3] = 0
#    data_Italia.iloc[max_idx:, 4] = 0
#    data_Italia.iloc[max_idx, 0] = pops['ITA'] - data_Italia.iloc[max_idx-1,-1] -data_Italia.iloc[max_idx-1,-2] - data_Italia.iloc[max_idx-1,5]
#data_Italia['prima_dose_tot'] = data_Italia.prima_dose.cumsum()
#data_Italia['seconda_dose_tot'] = data_Italia.seconda_dose.cumsum()
#data_Italia['mono_dose_tot'] = data_Italia.mono_dose.cumsum()
#data_Italia['pregressa_infezione_tot'] = data_Italia.pregressa_infezione.cumsum()
#data_Italia.loc[data_Italia.seconda_dose_tot > 0.95*data_Italia.prima_dose_tot, 'seconda_dose'] = data_Italia.loc[data_Italia.seconda_dose_tot > 0.95 * data_Italia.prima_dose_tot, 'prima_dose']
#data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'seconda_dose'] = data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'prima_dose']

#for n,i in enumerate(data_Italia.index):
#    if data_Italia.seconda_dose_tot[i] - data_Italia.mono_dose_tot[i] - data_Italia.pregressa_infezione_tot[i] > data_Italia.prima_dose_tot[i]:
#        data_Italia.iloc[n, 1] = data_Italia.iloc[n-1,5] - data_Italia.iloc[n-1,6] + data_Italia.iloc[n-1,-2] + data_Italia.iloc[n-1,-1]
#        data_Italia['seconda_dose_tot'] = data_Italia.seconda_dose.cumsum()



#data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'seconda_dose'] = data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'prima_dose_tot'] - data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'seconda_dose_tot'] 
#data_Italia.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

regions = [(a,x) for a, x in data.groupby(['area'])]
for a,x in regions:
    
    monodose = x[x['fornitore']=='Janssen']

    #x.drop(monodose.index, inplace=True)
    monodose = monodose.groupby('data_somministrazione').sum()
    x = x.groupby('data_somministrazione').sum()
    x['mono_dose'] = monodose['prima_dose']
    x['terza_dose'] = x.dose_addizionale_booster
    x.fillna(0,inplace=True)
    #x.loc[pd.to_datetime('2021-08-01'),['prima_dose','seconda_dose']] = 3e5
    #if a=='LOM':
    #    x.loc[pd.to_datetime(today),['terza_dose']] = 7.5e4 
    x.loc[max_Italia_index + pd.Timedelta(1, 'day')] = x.iloc[-7:,:].mean().round()
    data_reg = x.reindex(new_index, columns=['prima_dose', 'seconda_dose', 'terza_dose', 'pregressa_infezione', 'mono_dose']).ffill()
    data_reg['prima_dose_tot'] = data_reg.prima_dose.cumsum()
    data_reg['seconda_dose_tot'] = data_reg.seconda_dose.cumsum()
    data_reg.loc[data_reg.prima_dose_tot > pops[a], 'prima_dose'] = 0
    data_reg['prima_dose_tot'] = data_reg.prima_dose.cumsum()
    data_reg.loc[data_reg.seconda_dose_tot > data_reg.prima_dose_tot, 'seconda_dose'] = 0
    data_reg.loc[data_reg.seconda_dose_tot > data_reg.prima_dose_tot, 'prima_dose'] 
    #data_reg.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

    data_reg.to_csv('data/vaccini_regioni/' + sigla_regioni[a] + '_age.csv', index_label=['data','eta'])

data_Italia.to_csv('data/vaccines_age.csv', index_label=['data','eta'])
data_Italia.to_csv('data/vaccini_regioni/Italia_age.csv', index_label=['data','eta'])
