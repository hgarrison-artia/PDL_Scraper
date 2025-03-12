import pandas as pd
import tabula

A = 55.008
B = 51.48
C = 499.64
D = 682.03

tables = tabula.read_pdf('AK.pdf', area=[A,B,A+D,B+C], pages='all')

df = pd.concat(tables).reset_index(drop=True)
df.columns = ['Group', 'Market Basket', 'Product', 'Type', 'GNN', 'Strength', 'PDL Status', 'PDL Status Effective Date', 'Status Change from Previous']

print(df)

df.to_csv('AK_PDL.csv', index=False)