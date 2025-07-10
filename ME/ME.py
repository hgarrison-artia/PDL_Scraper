import pandas as pd
import numpy as np

df = pd.read_excel('ME.xlsx', 'SSDC-PDL_Maine-with-criteria')
df = df.iloc[16:].reset_index(drop=True)
df = df[['CATEGORY', 'PREFERRED DRUGS', 'NON-PREFERRED DRUGS       PA Required']]
df.columns = ['therapeutic_class', 'Preferred', 'Non-Preferred']
df = df.dropna(subset=['Preferred', 'Non-Preferred'], how='all')

df['therapeutic_class'] = df['therapeutic_class'].replace(r'^\s*$', np.nan, regex=True)
df['therapeutic_class'] = df['therapeutic_class'].ffill()
df = df.melt(id_vars='therapeutic_class', value_vars=['Preferred', 'Non-Preferred'], var_name='status', value_name='pdl_name')
df = df[['therapeutic_class', 'pdl_name', 'status']]
df['therapeutic_class'] = df['therapeutic_class'].str.lstrip()

df = df.dropna(subset=['pdl_name'])
df = df.sort_values('therapeutic_class').reset_index(drop=True)

df.to_csv('ME_PDL.csv', index=False)

