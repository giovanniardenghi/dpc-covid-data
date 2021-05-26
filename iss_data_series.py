## Import modules
import pandas as pd
import functools
import numpy as np

## Define variables
ignore_sex = True
sub = 0  # value replacing '<5'
save_csv = True
save_txt = True
age_groups = {'0-9': '0-19',
              '10-19': '0-19',
              '20-29': '20-39',
              '30-39': '20-39',
              '40-49': '40-59',
              '50-59': '40-59',
              '60-69': '60-79',
              '70-79': '60-79',
              '80-89': '80-89',
              '>90': '90+'}
#age_groups = 'Età'
state_group = {'Asintomatico':'Isolated',
               'Pauci-sintomatico': 'Isolated',
               'Lieve': 'Isolated',
               'Severo':'Hospitalized',
               'Critico':'Threatened'
               }

dates = pd.date_range(start='2020-12-08',end=np.datetime64('today','D'))
sesso_eta = pd.DataFrame(columns = ['iss_date','SESSO','AGE_GROUP','DECEDUTI','CASI_CUMULATIVI'])
stato_clinico = pd.DataFrame(columns = ['iss_date','SESSO','AGE_GROUP','STATO_CLINICO','CASI'])

for i in dates:
    try:
        tmp=pd.read_csv('https://raw.githubusercontent.com/floatingpurr/covid-19_sorveglianza_integrata_italia/main/data/'+i.strftime('%Y-%m-%d')+'/sesso_eta.csv')
        if tmp['iss_date'].values[0] not in sesso_eta['iss_date'].values:
            sesso_eta = sesso_eta.append(tmp)
        tmp=pd.read_csv('https://raw.githubusercontent.com/floatingpurr/covid-19_sorveglianza_integrata_italia/main/data/'+i.strftime('%Y-%m-%d')+'/stato_clinico.csv')
        if tmp['iss_date'].values[0] not in stato_clinico['iss_date'].values:
            stato_clinico = stato_clinico.append(tmp)
    except:
        pass
sesso_eta['iss_date'] = pd.to_datetime(sesso_eta['iss_date'], dayfirst=True)
stato_clinico['iss_date'] = pd.to_datetime(stato_clinico['iss_date'], dayfirst=True)

sesso_eta.rename(columns=dict(zip(sesso_eta.columns, ['Data', 'Sesso', 'Età', 'Deceduti', 'Casi'])), inplace=True)
sesso_eta.replace('<5', sub, inplace=True)
sesso_eta['Deceduti'] = pd.to_numeric(sesso_eta['Deceduti'])
sesso_eta['Casi'] = pd.to_numeric(sesso_eta['Casi'])
sesso_eta.set_index(['Data','Età', 'Sesso'], inplace=True)
sesso_eta.drop('Non noto', level=2, inplace=True)
sesso_eta.drop('Non noto', level=1, inplace=True)
#sesso_eta.drop('Casi',axis=1,inplace=True)

stato_clinico.rename(columns=dict(zip(stato_clinico.columns, ['Data', 'Sesso', 'Età', 'Stato', 'Casi'])), inplace=True)
stato_clinico.replace('<5', sub, inplace=True)
stato_clinico['Casi'] = pd.to_numeric(stato_clinico['Casi'])
stato_clinico['Stato'] = stato_clinico.Stato.str.capitalize()
stato_clinico.set_index(['Data','Età', 'Stato', 'Sesso'], inplace=True)
stato_clinico.drop('Non noto', level=1, inplace=True)

if ignore_sex:
    sesso_eta = sesso_eta.groupby(['Data',age_groups], level=[0,1]).sum()
    sesso_eta['Nuovi_Deceduti'] = sesso_eta.groupby(['Età'])['Deceduti'].diff()
    stato_clinico = stato_clinico.groupby([state_group, 'Data', age_groups], level=[2, 0, 1]).sum()
    sesso_eta['Casi'] = sesso_eta['Casi'] - sesso_eta['Deceduti'] - stato_clinico.xs('Isolated', level='Stato').values.flatten() - stato_clinico.xs('Hospitalized', level='Stato').values.flatten() - stato_clinico.xs('Threatened', level='Stato').values.flatten()
else:
    sesso_eta = sesso_eta.groupby(['Data', age_groups, 'Sesso'], level=[0, 1, 2]).sum()
    stato_clinico = stato_clinico.groupby(['Data', state_group, age_groups, 'Sesso'], level=[0, 2, 1, 3]).sum()

sesso_eta_perc = sesso_eta / sesso_eta.groupby('Data').sum()
stato_clinico_perc = stato_clinico / stato_clinico.groupby(['Stato','Data'],level=[0,1]).sum()

tmp = pd.concat({'Extinct': sesso_eta_perc['Deceduti']}, names=['Stato']).to_frame(name='Casi')
tmp3 = pd.concat({'Daily_extinct': sesso_eta_perc['Nuovi_Deceduti']}, names=['Stato']).to_frame(name='Casi')
tmp2 = pd.concat({'Recovered': sesso_eta_perc['Casi']}, names=['Stato']).to_frame(name='Casi')
stato_clinico_perc = stato_clinico_perc.append(tmp)
stato_clinico_perc = stato_clinico_perc.append(tmp2)
stato_clinico_perc = stato_clinico_perc.append(tmp3)


stato_clinico_perc = stato_clinico_perc.reset_index().pivot(index=['Data','Età'],columns='Stato',values='Casi')
new_index = pd.MultiIndex.from_product([pd.date_range(stato_clinico_perc.reset_index()['Data'].min(),stato_clinico_perc.reset_index()['Data'].max()),
                                        ['0-19','20-39','40-59','60-79','80-89','90+']], names=['Data','Età'] )
stato_clinico_perc = stato_clinico_perc.reindex(new_index)
stato_clinico_perc = stato_clinico_perc.unstack(1).ffill().stack()

#stato_clinico_perc.reset_index().drop('Età',axis=1).to_csv('stato_clinico.csv',index=None)
stato_clinico_perc.reset_index().to_csv('SUIHTER/stato_clinico.csv',index=None)
