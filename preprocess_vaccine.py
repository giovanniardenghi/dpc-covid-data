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

POPS = {
    'Italia':60483973,
    'Piemonte':4341375,
    'Valle d\'Aosta':125501,
    'Lombardia':10103969,
    'Veneto':4907704,
    'Friuli Venezia Giulia':1211357,
    'Liguria':1543127,
    'Emilia-Romagna':4467118,
    'Toscana':3722729,
    'Umbria':880285,
    'Marche':1518400,
    'Lazio':5865544,
    'Abruzzo':1305770,
    'Molise':302265,
    'Campania':5785861,
    'Puglia':4008296,
    'Basilicata':556934,
    'Calabria':1924701,
    'Sicilia':4968410,
    'Sardegna':1630474,
    'P.A. Bolzano':532080,
    'P.A. Trento':542739
}

data = pd.read_csv(
    'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
data_Italia = data.groupby('data_somministrazione').sum()
max_Italia_index = max(data_Italia.index)
new_max = max_Italia_index + pd.Timedelta(100, 'days')
new_index = pd.date_range('2020-02-24', new_max)

data_Italia.loc[max_Italia_index + pd.Timedelta(1, 'day')] = data_Italia.iloc[-7:, :].mean().round()
data_Italia = data_Italia.reindex(new_index, columns=['prima_dose', 'seconda_dose']).ffill()
data_Italia['prima_dose_tot'] = data_Italia.prima_dose.cumsum()
data_Italia['seconda_dose_tot'] = data_Italia.seconda_dose.cumsum()
data_Italia.loc[data_Italia.prima_dose_tot>0.9*POPS['Italia'],'prima_dose'] = 0
data_Italia.loc[data_Italia.seconda_dose_tot>0.9*POPS['Italia'],'seconda_dose'] = 0
data_Italia.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

regions = [(a,x) for a, x in data.groupby(['area'])]
for a,x in regions:
    
    x = x.groupby('data_somministrazione').sum()
    x.loc[max_Italia_index + pd.Timedelta(1, 'day')] = x.iloc[-7:,:].mean().round()
    data_reg = x.reindex(new_index, columns=['prima_dose', 'seconda_dose']).ffill()
    data_reg['prima_dose_tot'] = data_reg.prima_dose.cumsum()
    data_reg['seconda_dose_tot'] = data_reg.seconda_dose.cumsum()
    data_reg.loc[data_reg.prima_dose_tot>0.9*POPS[sigla_regioni[a]],'prima_dose'] = 0
    data_reg.loc[data_reg.seconda_dose_tot>0.9*POPS[sigla_regioni[a]],'seconda_dose'] = 0
    data_reg.drop(columns=['prima_dose_tot','seconda_dose_tot'],inplace=True)

    data_reg.to_csv('data/vaccini_regioni/' + sigla_regioni[a] + '.csv', index_label='data')

data_Italia.to_csv('data/vaccines.csv', index_label='data')
data_Italia.to_csv('data/vaccini_regioni/Italia.csv', index_label='data')
