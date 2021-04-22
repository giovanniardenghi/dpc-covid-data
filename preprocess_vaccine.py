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
data = pd.read_csv(
    'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')

data['data_somministrazione'] = pd.to_datetime(data['data_somministrazione'])
data_Italia = data.groupby('data_somministrazione').sum()
max_Italia_index = max(data_Italia.index)
new_max = max_Italia_index + pd.Timedelta(35, 'days')
new_index = pd.date_range('2020-02-24', new_max)

data_Italia.loc[max_Italia_index + pd.Timedelta(1, 'day')] = data_Italia.iloc[-7:, :].mean().round()
data_Italia = data_Italia.reindex(new_index, columns=['prima_dose', 'seconda_dose']).ffill()

regions = [(a,x) for a, x in data.groupby(['area'])]
for a,x in regions:
    x = x.groupby('data_somministrazione').sum()
    x.loc[max_Italia_index + pd.Timedelta(1, 'day')] = x.iloc[-7:,:].mean().round()
    data_reg = x.reindex(new_index, columns=['prima_dose', 'seconda_dose']).ffill()
    data_reg.to_csv('data/vaccini_regioni/' + sigla_regioni[a] + '.csv', index_label='data')

data_Italia.to_csv('data/vaccines.csv', index_label='data')
data_Italia.to_csv('data/vaccini_regioni/Italia.csv', index_label='data')
