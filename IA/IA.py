import pandas as pd
import docx

doc_path = 'IA.docx'
doc = docx.Document(doc_path)

matching_tables = []
for table in doc.tables:
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])
    df = pd.DataFrame(data)
    if df.shape[1] == 5:
        matching_tables.append(df)

combined_df = pd.concat(matching_tables, ignore_index=True)

therapeutic_category = None
records = []
for _, row in combined_df.iterrows():
    if row[0] not in ["B", "G", "O"] and row[0] != "PDL Categories":
        therapeutic_category = row[0]
    elif row[0] in ["B", "G", "O"]:
        pdl_name = row[3]
        for prefix in ["Step 1 - ", "Step 2 - ", "Step 3 - "]:
            if pdl_name.startswith(prefix):
                pdl_name = pdl_name[len(prefix):]
                break
        records.append({
            "pdl_name": pdl_name,
            "therapeutic_class": therapeutic_category,
            "pdl_status": row[2]
        })

def map_status(val):
    if val == "P" or val == "R":
        return "Preferred"
    elif val == "N" or val == "NR":
        return "Non-Preferred"
    return val

output_df = pd.DataFrame(records)
output_df["status"] = output_df["pdl_status"].apply(map_status)
final_df = output_df[["therapeutic_class", "pdl_name", "status"]]

final_df.to_csv("IA_PDL.csv", index=False)
