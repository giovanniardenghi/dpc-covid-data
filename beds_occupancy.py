import requests
import re
import ast
import pandas as pd

headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

r = requests.get('https://www.agenas.gov.it/covid19/web/index.php', headers=headers)

headers2 = re.search("\{(.*?)\}",r.text).group()

headers.update(ast.literal_eval(headers2))

resp = requests.get('https://www.agenas.gov.it/covid19/web/index.php?r=json%2Ftab2', auth=('Agenas', 'tab2-19'), headers=headers)

resp_json = resp.json()

columns = ['Regione', 'Ricoverati', 'PL_ricoveri', 'Terapie_intensive', 'PL_terapie_intensive', 'PL_TI_attivabili']

res_df = pd.DataFrame(columns=columns)

for reg in resp_json:
    res_df = res_df.append(dict(zip(columns,list(reg.values()))), ignore_index=True)

res_df = res_df.astype(dict(zip(columns[1:],['int32']*5)))

res_df['PL_occupati_perc'] = res_df['Ricoverati'] / res_df['PL_ricoveri'] * 100
res_df['TI_occupate_perc'] = res_df['Terapie_intensive'] / res_df['PL_terapie_intensive'] * 100

res_df.to_csv('data/occupazione_letti.csv', index=None)