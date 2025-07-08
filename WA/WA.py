import pandas as pd

cols_to_use = ['APPLE HEALTH DRUG CLASS', 'LABEL NAME', 'STRENGTH', 'DOSE FORM', 'PREFERRED STATUS']
df = pd.read_excel('WA.xlsx', usecols=cols_to_use, header=3)   # header=3 because the first 3 rows are not data

df = df.rename(columns={
    'APPLE HEALTH DRUG CLASS': 'therapeutic_class',
    'LABEL NAME': 'pdl_name',
    'STRENGTH': 'strength',
    'DOSE FORM': 'dose_form',
    'PREFERRED STATUS': 'status'
    })

df['pdl_name'] = df['pdl_name'] + ' ' + df['strength'].astype(str) + ' ' + df['dose_form']

status_map = {
    'P': 'Preferred',
    'N': 'Non-Preferred',
    'X': 'Non-PDL'
    }
df['status'] = df['status'].map(status_map)
df = df[df['status'] != 'Non-PDL']

df = df[['therapeutic_class', 'pdl_name', 'status']]

df.to_csv('WA_PDL.csv', index=False)