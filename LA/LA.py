import pandas as pd
import docx

doc_path = 'LA.docx'

doc = docx.Document(doc_path)

# Change the style of all text in table cells to "Normal"
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if paragraph.style.name != "Normal":
                    paragraph.style = doc.styles["Normal"]

all_tables = []

for table in doc.tables:
    data = []

    for row in table.rows:
        # Remove unnecessary texts from the table: these do not translate well when converted to csv file
        for cell in row.cells:
            if '®' in cell.text:
                cell.text = cell.text.replace('®', '')
            if '™' in cell.text:
                cell.text = cell.text.replace('™', '')
            if '*Request Form' in cell.text:
                cell.text = cell.text.replace('*Request Form', '')
            if '*Criteria' in cell.text:
                cell.text = cell.text.replace('*Criteria', '')
            if '*POS Edits' in cell.text:
                cell.text = cell.text.replace('*POS Edits', '')

        data.append([cell.text.strip() for cell in row.cells])  # Extract text from each cell

    if data:  # Proceed only if the table has non-empty rows
        df = pd.DataFrame(data)  # Convert to DataFrame
        df.columns = df.iloc[0]
        df = df[1:]

        # Remove rows where all columns are empty
        df = df.dropna(how='all')

        if "Drugs on PDL" in df.columns and "Drugs on NPDL which Require Prior Authorization (PA)" in df.columns:
            df = df.rename(columns={"Drugs on PDL": "Preferred", "Drugs on NPDL which Require Prior Authorization (PA)": "Non-Preferred"})
            all_tables.append(df)

final_df = pd.concat(all_tables).reset_index(drop=True)
print(final_df)
final_df.to_csv('../LA_PDL.csv', index=False, encoding='utf-8-sig')  # Use utf-8-sig to avoid BOM character