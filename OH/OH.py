import pandas as pd
import openpyxl
import docx
from docx.oxml.ns import qn

doc_path = 'OH.docx' 
doc = docx.Document(doc_path)

class_color = '002F86'
redrow_color = 'AB2228'
subclass_color = 'FFC500'
Class = None
Subclass = None
table_data = []


for table_idx, table in enumerate(doc.tables):
    Class = None
    Subclass = None
    for row in table.rows:
        row_values = [cell.text.strip() for cell in row.cells if cell.text.strip()]
        row_class = None
        # Only combine if not all cell values are identical
        if row_values and not all(val == row_values[0] for val in row_values):
            for cell in row.cells:
                shd = cell._tc.xpath('.//w:shd')
                fill = shd[0].get(qn('w:fill')) if shd else None
                if fill == class_color:
                    row_class = "".join(row_values)
                    break
        else:
            for cell in row.cells:
                shd = cell._tc.xpath('.//w:shd')
                fill = shd[0].get(qn('w:fill')) if shd else None
                if fill == class_color:
                    row_class = row_values[0]
                    break
        if row_class:
            Class = row_class
            Subclass = None  # Optionally reset Subclass when a new Class is found
        for idx, cell in enumerate(row.cells):
            value = cell.text.strip()
            shd = cell._tc.xpath('.//w:shd')
            fill = shd[0].get(qn('w:fill')) if shd else None
            if fill == subclass_color and value:
                Subclass = value
            elif fill != class_color and fill != subclass_color and value and idx != len(row.cells) - 1:
                # Split on \n and append each drug
                for drug in value.split('\n'):
                    drug = drug.strip()
                    if drug and Class and Class != 'Example Category' and fill != redrow_color:
                        status = "Preferred" if idx == 0 else "Non-Preferred"
                        table_data.append([Class, Subclass, drug, status])

df = pd.DataFrame(table_data, columns=['therapeutic_class', 'Subclass', 'pdl_name', 'status'])
df['therapeutic_class'] = df['therapeutic_class'].fillna('') + ': ' + df['Subclass'].fillna('')
df = df.drop(['Subclass'], axis=1)

df.to_csv('OH_PDL.csv', index=False)