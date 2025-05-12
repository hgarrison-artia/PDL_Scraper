import pandas as pd
import docx
import re

doc_path = 'AL.docx'
doc = docx.Document(doc_path)

records = []
current_therapeutic_class = None

def clean_drug_name(drug):
    # First remove any newlines and extra spaces
    drug = drug.replace('\n', ' ').strip()
    drug = re.sub(r'\s+', ' ', drug)
    # Remove TIM from the end (case insensitive)
    drug = re.sub(r'\s+TIM$', '', drug, flags=re.IGNORECASE)
    drug = re.sub(r'\s+CC$', '', drug, flags=re.IGNORECASE)
    drug = re.sub(r'\s+CC,$', '', drug, flags=re.IGNORECASE)
    # Remove * and ^ characters
    drug = drug.replace('*', '').replace('^', '')
    return drug

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
        # Clean therapeutic class: remove newlines, extra spaces, and split at †
        therapeutic_class = therapeutic_class.replace('\n', ' ').strip()
        therapeutic_class = re.sub(r'\s+', ' ', therapeutic_class)  # Replace multiple spaces with single space
        therapeutic_class = therapeutic_class.split('†',1)[0].strip()

        if therapeutic_class and therapeutic_class.lower() != 'none':
            current_therapeutic_class = therapeutic_class

        if not current_therapeutic_class:
            continue

        for idx in no_pa_idxs:
            drug = row[idx]
            if drug and drug.lower() != 'none':
                # Clean the drug name before adding to records
                cleaned_drug = clean_drug_name(drug)
                records.append({
                    'therapeutic_class': current_therapeutic_class,
                    'pdl_name': cleaned_drug,
                    'status': 'Preferred'
                })

        drug = row[pa_required_idx]
        if drug and drug.lower() != 'none':
            # Clean the drug name before adding to records
            cleaned_drug = clean_drug_name(drug)
            records.append({
                'therapeutic_class': current_therapeutic_class,
                'pdl_name': cleaned_drug,
                'status': 'Non-Preferred'
            })

# Remove the expansion logic since we want to keep drug names intact
df = pd.DataFrame(records)
df_clean = df[df['therapeutic_class'].str.upper() != 'DRUG CLASS'].reset_index(drop=True)

# Final cleanup of therapeutic classes
df_clean['therapeutic_class'] = df_clean['therapeutic_class'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

# One final pass to ensure no TIM remains
df_clean['pdl_name'] = df_clean['pdl_name'].apply(lambda x: re.sub(r'TIM$', '', x, flags=re.IGNORECASE))

df_clean['pdl_name'] = df_clean['pdl_name'].apply(lambda x: re.sub(r'CC$', '', x, flags=re.IGNORECASE))

df_clean['pdl_name'] = df_clean['pdl_name'].apply(lambda x: re.sub(r'CC,$', '', x, flags=re.IGNORECASE))

# Remove any rows where pdl_name is empty
df_clean = df_clean[df_clean['pdl_name'].str.strip() != '']

# Remove any rows where pdl_name contains "continued"
df_clean = df_clean[~df_clean['pdl_name'].str.contains('continued', case=False, na=False)]

# Final cleanup to remove * and ^ characters
df_clean['pdl_name'] = df_clean['pdl_name'].apply(lambda x: x.replace('*', '').replace('^', ''))

df_clean.to_csv('AL_PDL.csv', index=False)