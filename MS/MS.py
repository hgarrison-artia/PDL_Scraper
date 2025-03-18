import pandas as pd
import docx

doc_path = 'MS.docx'

doc = docx.Document(doc_path)
all_tables = []

def get_first_two_unique_columns(df):
    # Ensure there are at least two columns
    if df.shape[1] < 2:
        raise ValueError("DataFrame must have at least two columns")
    
    first_col = df.iloc[:, 0]  # Always take the first column
    selected_columns = [first_col]
    
    # Iterate through remaining columns to find a unique second column
    for i in range(1, df.shape[1]):
        candidate_col = df.iloc[:, i]
        
        # Ignore the first 3 rows when checking for uniqueness
        if not first_col.iloc[3:].equals(candidate_col.iloc[3:]):
            selected_columns.append(candidate_col)
            break
    
    # If we couldn't find a second unique column, raise an error
    if len(selected_columns) < 2:
        raise ValueError("Could not find two unique columns in the DataFrame")
    
    # Create new DataFrame with selected columns
    return pd.DataFrame({"Col1": selected_columns[0], "Col2": selected_columns[1]})


for table in doc.tables:
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])  # Extract text from each cell

    df = pd.DataFrame(data)  # Convert to DataFrame
    df.columns = df.iloc[0]
    df = df[1:]

    new_df = get_first_two_unique_columns(df)

    new_df.columns = ['PREFERRED AGENTS', 'NON-PREFERRED AGENTS']


    same_value_rows = new_df[new_df.apply(lambda x: x.nunique() == 1, axis=1)]
    df_filtered = new_df.drop(same_value_rows.index).reset_index(drop=True)

    all_tables.append(df_filtered)

final_df = pd.concat(all_tables).reset_index(drop=True)
print(final_df)
final_df.to_csv('MS_PDL.csv', index=False)