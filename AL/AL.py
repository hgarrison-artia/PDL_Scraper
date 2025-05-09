import pandas as pd
import docx
import re

doc_path = 'AL.docx'
doc = docx.Document(doc_path)

records = []
current_therapeutic_class = None

for table in doc.tables:
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
    if not rows:
        continue

    # Dynamically find the header row (contains DRUG CLASS and PA columns)
    header_row_index = -1
    for i, row in enumerate(rows):
        upper_row = [cell.upper() for cell in row]
        if 'DRUG CLASS' in upper_row and 'PA REQUIRED' in upper_row:
            header_row_index = i
            break

    if header_row_index == -1:
        continue

    header_row = [cell.upper() for cell in rows[header_row_index]]
    try:
        class_idx = header_row.index('DRUG CLASS')
        no_pa_idxs = [i for i, h in enumerate(header_row) if 'NO PA REQUIRED' in h]
        pa_required_idx = header_row.index('PA REQUIRED')
    except ValueError:
        continue

    for row in rows[header_row_index + 1:]:
        if len(row) < max(no_pa_idxs + [pa_required_idx]) + 1:
            continue

        therapeutic_class = row[class_idx]
        therapeutic_class = therapeutic_class.split('†',1)[0]

        if therapeutic_class and therapeutic_class.lower() != 'none':
            current_therapeutic_class = therapeutic_class

        if not current_therapeutic_class:
            continue

        for idx in no_pa_idxs:
            drug = row[idx]
            if drug and drug.lower() != 'none':
                records.append({
                    'therapeutic_class': current_therapeutic_class,
                    'pdl_name': drug,
                    'status': 'Preferred'
                })

        drug = row[pa_required_idx]
        if drug and drug.lower() != 'none':
            records.append({
                'therapeutic_class': current_therapeutic_class,
                'pdl_name': drug,
                'status': 'Non-Preferred'
            })

expanded_records = []

for record in records:
    clean_text = record['pdl_name'].replace('\n', ' ').strip()
    clean_text = re.sub(r'\s+and\s+', ', ', clean_text)
    drugs = [d.strip() for d in clean_text.split(',') if d.strip().lower() != 'none']

    for drug in drugs:
        expanded_records.append({
            'therapeutic_class': record['therapeutic_class'],
            'pdl_name': drug,
            'status': record['status']
        })

df = pd.DataFrame(expanded_records)
df_clean = df[df['therapeutic_class'].str.upper() != 'DRUG CLASS'].reset_index(drop=True)

df_clean.to_csv('AL_PDL.csv', index=False)