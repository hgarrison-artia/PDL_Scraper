import pandas as pd
import docx

doc_path = 'OR PDL.docx' 
doc = docx.Document(doc_path)

all_rows = []

for table in doc.tables:
    for row in table.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        all_rows.append(row_data)

df = pd.DataFrame(all_rows)


df[0] = df[0].replace('', pd.NA).ffill()
df[1] = df[1].replace('', pd.NA).ffill()

df[2] = df[2].astype(str).str.strip() + ' ' + df[3].astype(str).str.strip()
df = df.drop(columns=[3])

df['Status'] = 'Preferred'
df = df.iloc[1:].reset_index(drop=True)
df[0] = df[0].astype(str).str.strip() + ': ' + df[1].astype(str).str.strip()
df = df.drop(columns=[1])

df.columns = ['therapeutic_class', 'pdl_name', 'status']
df = df[~df['therapeutic_class'].str.strip().str.startswith('System')].reset_index(drop=True)
df['pdl_name'] = [name.replace("\n", " ") for name in df['pdl_name']]
df['therapeutic_class'] = [name.replace("\n", " ") for name in df['therapeutic_class']]

df.to_csv('OR_PDL.csv', index=False)

