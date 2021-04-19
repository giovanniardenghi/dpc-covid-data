import pandas as pd

data_Italy = pd.read_csv("data/andamento_nazionale.csv",engine='c')
data_Regions = pd.read_csv("data/regioni.csv",engine='c')

regions = [x for _, x in data_Regions.groupby('denominazione_regione')]
for x in regions:
    x.reset_index(drop=True,inplace=True)
    x.to_csv('data/regioni/'+x.denominazione_regione[0]+'.csv',index=None)

data_Italy['denominazione_regione']='Italia'
data_Italy.to_csv('data/regioni/Italia.csv',index=None)
