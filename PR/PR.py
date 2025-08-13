import docx
import pandas as pd
import os
import re

docx_dir = 'PDLs_docx_converted'

output_rows = []
for filename in os.listdir(docx_dir):
    if filename.lower().endswith('.docx') and not filename.startswith('~$'):
        docx_path = os.path.join(docx_dir, filename)
        doc = docx.Document(docx_path)
        header = None
        subheader = None
        for table in doc.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]

                # If all values in the row are the same and not empty, check for header/subheader
                if len(cells) > 0 and all(cell == cells[0] and cell != "" for cell in cells):
                    value = cells[0]
                    if value.isupper():
                        header = value
                        subheader = None
                    else:
                        subheader = value
                    continue
                # therapeutic_class string
                if header and subheader:
                    therapeutic_class = f"{header}: {subheader}"
                elif header:
                    therapeutic_class = header
                else:
                    therapeutic_class = ""
                therapeutic_class = re.sub(r'\[.*?\]', '', therapeutic_class).strip()

                # Drug name: first cell, or second if first is empty, or if first and second are the same, just use one
                drug_name = ""
                if len(cells) >= 2 and cells[0] == cells[1]:
                    drug_name = cells[0]
                elif len(cells) > 0 and cells[0]:
                    drug_name = cells[0]
                elif len(cells) > 1 and cells[1]:
                    drug_name = cells[1]

                # Status: look for 'Preferred' or 'Non-Preferred' in any cell
                status = ""
                for cell in cells:
                    if cell.lower() in ["preferred", "non-preferred"]:
                        status = cell
                        break

                if drug_name and drug_name != therapeutic_class and drug_name != "-":
                    output_rows.append([therapeutic_class, drug_name, status])
        print(f'Processed file: {filename}')

output_df = pd.DataFrame(output_rows, columns=["therapeutic_class", "pdl_name", "status"])
output_df = output_df.drop_duplicates(subset=["therapeutic_class", "pdl_name", "status"])
output_df = output_df[output_df['status'].str.strip() != '']
output_df['pdl_name'] = [name.replace('\n','') for name in output_df['pdl_name']]

output_df.to_csv('PR_PDL.csv', index=False)