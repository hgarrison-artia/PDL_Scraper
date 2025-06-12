import pandas as pd

df = pd.read_excel('AK.xlsx')

df.columns = ['Group', 'therapeutic_class', 'pdl_name', 'Type', 'GNN', 'Strength', 'status', 'PDL Status Effective Date', 'Status Change from Previous']

df['pdl_name'] = df['pdl_name'] + ': ' + df['Strength'].astype(str)

df['status'] = ['Preferred' if status == 'ON' else 'Non-Preferred' for status in df['status']]

df = df[['therapeutic_class', 'pdl_name', 'status']]

df.to_csv('AK_PDL.csv', index=False)