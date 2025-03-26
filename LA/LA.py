import pandas as pd
import docx
import re

doc_path = 'LA.docx'

doc = docx.Document(doc_path)

# Change the style of all text in table cells to "Normal" because the original style is not preserved when converting to csv
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if paragraph.style.name != "Normal":
                    paragraph.style = doc.styles["Normal"]

all_tables = []

def clean_text(text):
    text = text.strip()

    # Remove text after "(number)"
    text = re.sub(r"\(\d+\).*", "", text)  
    text = re.sub(r"\(\d+\)", "", text)  

    if "Potency" in text:
        return "Steroids, Topical"

    return text.strip()

def is_all_caps(text):
    return text.isupper() and any(c.isalpha() for c in text)

for table in doc.tables:
    data = []

    for row in table.rows:
        row_data = []

        # Remove unnecessary symbols and texts
        for i, cell in enumerate(row.cells):
            cell_text = cell.text.strip()

            for text_to_remove in ["®", "™", "*Request Form", "*Criteria", "*POS Edits", "Continued"]:
                cell_text = cell_text.replace(text_to_remove, "")
            if "REQUEST FORM" in cell_text:
                cell_text = ""

            if i == 0:
                cell_text = clean_text(cell_text)
            row_data.append(cell_text)

        data.append(row_data)

    if data:
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]  # Set first row as column headers
        df = df[1:] # Remove first row

        # Convert empty strings to NaN and remove rows where all columns are empty
        df.replace("", pd.NA, inplace=True)
        df.dropna(how="all", inplace=True)

        if "Drugs on PDL" in df.columns and "Drugs on NPDL which Require Prior Authorization (PA)" in df.columns:
            df = df.rename(columns={"Descriptive Therapeutic Class": "Therapeutic Class", 
                                    "Drugs on PDL": "Preferred", 
                                    "Drugs on NPDL which Require Prior Authorization (PA)": "Non-Preferred"})

            if not df.empty:

                # Fill down the first column (Therapeutic Class)
                first_col = df.columns[0]
                df[first_col] = df[first_col].ffill()

                new_values = df[first_col].tolist()
                for i in range(len(new_values) - 1):  # Skip the last row to avoid out-of-range error
                    if is_all_caps(new_values[i]) and not is_all_caps(new_values[i + 1]):
                        new_values[i] = new_values[i + 1]  # Replace ALL CAPS with next valid value

                df[first_col] = new_values  # Assign modified list back to DataFrame

                df = df[df["Preferred"] != df["Non-Preferred"]]  # Remove rows where Preferred and Non-Preferred are the same

            all_tables.append(df)

final_df = pd.concat(all_tables).reset_index(drop=True)
print(final_df)
final_df.to_csv('../LA_PDL.csv', index=False, encoding='utf-8-sig')  # Use utf-8-sig to avoid BOM character