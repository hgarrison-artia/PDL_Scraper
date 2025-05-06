import pandas as pd
import docx
import re

doc_path = 'LA.docx'

doc = docx.Document(doc_path)

all_tables = []

for table in doc.tables:
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])  # Extract text from each cell

    df = pd.DataFrame(data)  # Convert to DataFrame
    df.columns = df.iloc[0,:]
    df = df[1:]
    if df.shape[1] == 3:
        all_tables.append(df)

final_df = pd.concat(all_tables).reset_index(drop=True)

final_df['Descriptive Therapeutic Class'] = [re.sub(r' \(\d+\)', '', i) for i in final_df['Descriptive Therapeutic Class']]
final_df['Descriptive Therapeutic Class'] = ['' if re.search('[a-z]', i) else i for i in final_df['Descriptive Therapeutic Class']]
final_df['Descriptive Therapeutic Class'] = ['' if re.search('[*]', i) else i for i in final_df['Descriptive Therapeutic Class']]
final_df['Descriptive Therapeutic Class'] = [i.replace('\n', '') for i in final_df['Descriptive Therapeutic Class']]

final_df['Drugs on PDL'] = [i.replace('®', '') for i in final_df['Drugs on PDL']]
final_df['Drugs on PDL'] = [i.replace('NONE', '') for i in final_df['Drugs on PDL']]
final_df['Drugs on PDL'] = [i.replace('™', '') for i in final_df['Drugs on PDL']]


final_df['Drugs on NPDL which Require Prior Authorization (PA)'] = [i.replace('®', '') for i in final_df['Drugs on NPDL which Require Prior Authorization (PA)']]
final_df['Drugs on NPDL which Require Prior Authorization (PA)'] = [i.replace('NONE', '') for i in final_df['Drugs on NPDL which Require Prior Authorization (PA)']]
final_df['Drugs on NPDL which Require Prior Authorization (PA)'] = [i.replace('™', '') for i in final_df['Drugs on NPDL which Require Prior Authorization (PA)']]

last_class = ''

for _, row in final_df.iterrows():
    if final_df.loc[_, 'Descriptive Therapeutic Class'] == '':
        final_df.loc[_, 'Descriptive Therapeutic Class'] = last_class
    else:
        last_class = final_df.loc[_, 'Descriptive Therapeutic Class']
    

final_df.columns = ['therapeutic_class', 'Preferred', 'Non-Preferred']

df_melted = final_df.melt(
    id_vars=['therapeutic_class'],    
    value_vars=['Preferred', 'Non-Preferred'],    
    var_name='status',                        
    value_name='pdl_name'                       
)

df_melted = df_melted[df_melted['pdl_name'].str.strip() != ''].reset_index(drop=True)

df_melted.to_csv('LA_PDL.csv', index=False)
