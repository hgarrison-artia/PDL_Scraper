import pandas as pd
import tabula

A = 176.328
B = 52.128
C = 498.87
D = 544.33

tables = tabula.read_pdf('GA.pdf', area=[A,B,A+D,B+C], pages='all')

df = pd.concat(tables).reset_index(drop=True)
df.columns = ['Drug', 'Preferred', 'Non-Preferred', 'PA', 'QLL']

print(df)

df.to_csv('GA_PDL.csv', index=False)