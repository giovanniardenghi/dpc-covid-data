import pandas as pd

gp = pd.read_csv('https://raw.githubusercontent.com/ministero-salute/it-dgc-opendata/master/data/dgc-issued.csv')

gp['data'] = pd.to_datetime(gp.data)
gp.set_index('data', inplace=True)
gp.sort_index(inplace=True)
gp.loc[pd.to_datetime('2020-02-24')] = 0
gp.loc[gp.index.max() + pd.Timedelta(1, 'day')] = gp.iloc[-7:, :].mean().round()
gp = gp.reindex(pd.date_range('2020-02-24', gp.index.max()+pd.Timedelta(100,'days'))).ffill()
gp.issued_for_tests.to_csv('data/gp_from_test.csv',index_label='data')
