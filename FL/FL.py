import pandas as pd

df = pd.read_excel('FL.xlsx')
df.columns = ['HIC', 'Therapeutic Class', 'Label Name', 'Generic Name', 'Min Age', 'Max Age', 'PA']
df = df[5:].reset_index(drop=True)
last_class = ''

for _, row in df.iterrows():
    if pd.isna(df.loc[_, 'Therapeutic Class']):
        df.loc[_, 'Therapeutic Class'] = last_class
    else:
        last_class = df.loc[_, 'Therapeutic Class']
    
df = df[['Therapeutic Class', 'Label Name']]
df.columns = ['therapeutic_class', 'pdl_name']
df['status'] = 'Preferred'

df.to_csv('FL_PDL.csv', index=False)