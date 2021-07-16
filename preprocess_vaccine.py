import pandas as pd
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

data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
monodose = data[data['fornitore']=='Janssen']

#data.drop(monodose.index, inplace=True)
monodose = monodose.groupby('data_somministrazione').sum()
data_Italia = data.groupby('data_somministrazione').sum()
data_Italia['mono_dose'] = monodose['prima_dose']
data_Italia.fillna(0,inplace=True)

max_Italia_index = max(data_Italia.index)
new_max = max_Italia_index + pd.Timedelta(100, 'days')
new_index = pd.date_range('2020-02-24', new_max)

data_Italia.loc[pd.to_datetime('2021-08-01'),['prima_dose','seconda_dose']] = 3e5
data_Italia.loc[max_Italia_index + pd.Timedelta(1, 'day')] = data_Italia.iloc[-7:, :].mean().round()
data_Italia = data_Italia.reindex(new_index, columns=['prima_dose', 'seconda_dose', 'pregressa_infezione', 'mono_dose']).ffill()
data_Italia['prima_dose_tot'] = data_Italia.prima_dose.cumsum()
data_Italia['seconda_dose_tot'] = data_Italia.seconda_dose.cumsum()
data_Italia.loc[data_Italia.prima_dose_tot > pops['ITA'], 'prima_dose'] = 0
data_Italia['prima_dose_tot'] = data_Italia.prima_dose.cumsum()
#data_Italia.loc[data_Italia.seconda_dose_tot > 0.95*data_Italia.prima_dose_tot, 'seconda_dose'] = data_Italia.loc[data_Italia.seconda_dose_tot > 0.95 * data_Italia.prima_dose_tot, 'prima_dose']
data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'seconda_dose'] = data_Italia.loc[data_Italia.seconda_dose_tot > data_Italia.prima_dose_tot, 'prima_dose']
data_Italia.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

regions = [(a,x) for a, x in data.groupby(['area'])]
for a,x in regions:
    
    monodose = x[x['fornitore']=='Janssen']

    #x.drop(monodose.index, inplace=True)
    monodose = monodose.groupby('data_somministrazione').sum()
    x = x.groupby('data_somministrazione').sum()
    x['mono_dose'] = monodose['prima_dose']
    x.fillna(0,inplace=True)
    #x.loc[pd.to_datetime('2021-08-01'),['prima_dose','seconda_dose']] = 3e5
    x.loc[max_Italia_index + pd.Timedelta(1, 'day')] = x.iloc[-7:,:].mean().round()
    data_reg = x.reindex(new_index, columns=['prima_dose', 'seconda_dose', 'pregressa_infezione', 'mono_dose']).ffill()
    data_reg['prima_dose_tot'] = data_reg.prima_dose.cumsum()
    data_reg['seconda_dose_tot'] = data_reg.seconda_dose.cumsum()
    data_reg.loc[data_reg.prima_dose_tot > pops[a], 'prima_dose'] = 0
    data_reg['prima_dose_tot'] = data_reg.prima_dose.cumsum()
    data_reg.loc[data_reg.seconda_dose_tot > data_reg.prima_dose_tot, 'seconda_dose'] = 0
    data_reg.loc[data_reg.seconda_dose_tot > data_reg.prima_dose_tot, 'prima_dose'] 
    data_reg.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

    data_reg.to_csv('data/vaccini_regioni/' + sigla_regioni[a] + '.csv', index_label='data')

data_Italia.to_csv('data/vaccines.csv', index_label='data')
data_Italia.to_csv('data/vaccini_regioni/Italia.csv', index_label='data')
