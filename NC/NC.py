import pandas as pd
import openpyxl

wb = openpyxl.load_workbook("NC.xlsx")
ws = wb["Table 1"]

Class_Color = 'FF99CCFF'
Subclass_Color = 'FFBEBEBE'
Sub2class_Color = 'FFD9D9D9'
other_Color = 'FFF1F1F1'
Class = None
Subclass = None
Sub2class = None
drugs = []



for row in ws.iter_rows():
    for idx, cell in enumerate(row):
        value = cell.value
        fill = cell.fill
        if value and isinstance(value, str):
            if '- T/F' in value:
                value = value.split('- T/F')[0].strip()
            elif '- Clinical' in value:
                value = value.split('- Clinical')[0].strip()
        if fill and fill.fill_type == 'solid' and fill.start_color.rgb == Class_Color:
            Class = value
        elif fill and fill.fill_type == 'solid' and fill.start_color.rgb == Subclass_Color:
            Subclass = value
        elif fill and fill.fill_type == 'solid' and fill.start_color.rgb == Sub2class_Color:
            Sub2class = value
        drug = None
        if value and not fill.fill_type == 'solid' and cell.coordinate not in ws.merged_cells:
            drug = value
        status = None
        if idx == 0:
            status = "Preferred"
        elif idx == 1:
            status = "Non-Preferred"
        if drug and Class and status:
            drugs.append([Class, Subclass, Sub2class, drug, status])

df = pd.DataFrame(drugs, columns=['therapeutic_class', 'Subclass', 'Sub2class', 'pdl_name', 'status'])
df = df[df['therapeutic_class'].str.strip().str.upper() != 'DIABETIC SUPPLIES']
# Drop drugs that are identical to any class, subclass, or sub2class
mask = ~(
    (df['pdl_name'] == df['therapeutic_class']) |
    (df['pdl_name'] == df['Subclass']) |
    (df['pdl_name'] == df['Sub2class'])
)
df = df[mask]

df = df[~df['pdl_name'].str.lower().isin(['preferred', 'non-preferred'])]
df['therapeutic_class'] = df['therapeutic_class'].fillna('') + ': ' + df['Subclass'].fillna('') + ': ' + df['Sub2class'].fillna('')
df = df.drop(['Subclass', 'Sub2class'], axis=1)

df = df[df['pdl_name'].str.len() <= 200]

df.to_csv('NC_PDL.csv', index=False)