import pandas as pd
import docx
import re

# Function to clean up text
def clean_text(text):
    text = text.strip()

    for text_to_remove in ["®", "™", "*Request Form", "*Criteria", "*POS Edits"]:
        text = text.replace(text_to_remove, "")

    text = re.sub(r"\(\d+\).*", "", text)
    text = re.sub(r"\(\d+\)", "", text)

    if "REQUEST FORM" in text or "listed on page" in text:
        text = ""

    return text

doc_path = "LA.docx"
doc = docx.Document(doc_path)

all_tables = []

# Preprocessing: changing text style in the table for converted csv file
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if paragraph.style.name != "Normal":
                    paragraph.style = doc.styles["Normal"]

    data = []

    for row in table.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        data.append(row_data)

    if data:
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.applymap(lambda x: clean_text(x) if isinstance(x, str) else x)
    else:
        df = pd.DataFrame()

    # Converting empty strings to NaN and removing rows where all columns are empty
    df.replace("", pd.NA, inplace=True)
    df.dropna(how="all", inplace=True)

    # Modifying cells containing the word "Potency"; this is a special case for Steroids category
    df = df.apply(lambda col: col.map(lambda x: f"Steroids, Topical - {x}" if isinstance(x, str) and "Potency" in x else x))
    
    if not df.empty and set(["Drugs on PDL", "Drugs on NPDL which Require Prior Authorization (PA)"]).issubset(df.columns):
        df = df.rename(columns={"Descriptive Therapeutic Class": "Therapeutic Class", 
                                "Drugs on PDL": "Preferred", 
                                "Drugs on NPDL which Require Prior Authorization (PA)": "Non-Preferred"})
        if not df.empty:
            # Fill down the first column with a corresponding subheading
            first_col = df.columns[0]
            df[first_col] = df[first_col].ffill()

            new_values = df[first_col].tolist()     
            for i in range(len(new_values) - 1):
                # If there is a cell "Steroids, Topical", check if there is a unique value for the next cells and replace the cell with it
                unique_value_steroids = None
                for j in range(i + 1, len(new_values)):
                    if isinstance(new_values[j], str) and new_values[j].startswith("Steroids, Topical") and new_values[j] != "Steroids, Topical":
                        unique_value_steroids = new_values[j]
                        break
                if unique_value_steroids:
                    for k in range(i, j):
                        new_values[k] = unique_value_steroids
    
            for i in range(len(new_values) - 1):
                if isinstance(new_values[i], str) and str(new_values[i]).isupper():
                    sub_heading = None
                    sub_sub_heading = None
    
                    for j in range(i+1, len(new_values)):
                        if isinstance(new_values[j], str) and not str(new_values[j]).isupper():
                            if sub_heading is None:
                                sub_heading = new_values[j]
                            elif new_values[j] != sub_heading:
                                sub_sub_heading = new_values[j]
                                break
    
                    replacement_value = sub_sub_heading if sub_sub_heading else sub_heading
    
                    if replacement_value:
                        for k in range(i,j):
                            new_values[k] = replacement_value
    
            df[first_col] = new_values
            df.replace("NONE", "", inplace=True)
    
            # Remove rows where both "Preferred" and "Non-Preferred" columns are empty
            df.dropna(subset=[df.columns[1], df.columns[2]], how="all", inplace=True)
            # Remove rows where "Preferred" and "Non-Preferred" columns are ALL CAPS and have the same value
            df = df[~((df["Preferred"].str.isupper()) & (df["Non-Preferred"].str.isupper()) & (df["Preferred"] == df["Non-Preferred"]))]
    
            all_tables.append(df)

final_df = pd.concat(all_tables).reset_index(drop=True)

df_melted = pd.melt(
    final_df,
    id_vars=['Therapeutic Class'],
    value_vars=['Preferred', 'Non-Preferred'],
    var_name='status',
    value_name='pdl_name'
)

# Remove rows where the drug name is null or empty.
df_melted = df_melted.dropna(subset=['pdl_name'])
df_melted = df_melted[df_melted['pdl_name'].str.strip() != ""]

# Rename the therapeutic class column to match the desired output.
df_melted = df_melted.rename(columns={'Therapeutic Class': 'therapeutic_class'})

df_melted.to_csv('LA_PDL.csv', index=False, encoding='utf-8-sig')  # Use utf-8-sig to avoid BOM character