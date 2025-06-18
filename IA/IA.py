import pandas as pd
import docx

doc_path = 'IA.docx'
doc = docx.Document(doc_path)

header_keywords = ["B, G or O", "Comment", "P, N, R or NR", "Therapeutic Category", "PA Form Link"]

matching_tables = []
for table in doc.tables:
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])
    df = pd.DataFrame(data)
    if df.shape[0] > 0 and all(keyword in df.iloc[0].tolist() for keyword in header_keywords):
        matching_tables.append(df)

combined_df = pd.concat(matching_tables, ignore_index=True)
combined_df = combined_df[~((combined_df.iloc[:, 0] == 'PDL Categories') & (combined_df.iloc[:, 1] == 'PDL Categories'))]

therapeutic_category = None
records = []
for _, row in combined_df.iterrows():
    if row[0] in ["B", "G", "O"]:
        records.append({
            "pdl_name": row[3],
            "therapeutic_class": therapeutic_category,
            "pdl_status": row[2]
        })
    else:
        therapeutic_category = row[0]

def map_status(val):
    if val == "P":
        return "Preferred"
    elif val == "N":
        return "Non-Preferred"
    elif val == "R":
        return "Preferred"
    elif val == "NR":
        return "Non-Preferred"
    return val

output_df = pd.DataFrame(records)
output_df["status"] = output_df["pdl_status"].apply(map_status)
final_df = output_df[["therapeutic_class", "pdl_name", "status"]]

final_df.to_csv("IA_PDL.csv", index=False)
