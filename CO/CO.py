import pandas as pd
import docx

doc_path = 'CO.docx'

doc = docx.Document(doc_path)
all_tables = []
i = 0


def remove_zero_rows(df):
    return df[~((df.iloc[:, 0] == '') & (df.iloc[:, 1] == ''))]


def get_first_two_unique_columns(df, i):
    # Ensure there are at least two columns
    if df.shape[1] < 2:
        raise ValueError("DataFrame must have at least two columns")


    df = remove_zero_rows(df)
    
    first_col = df.iloc[:, 0]  # Always take the first column
    selected_columns = [first_col]

    # Iterate through remaining columns to find a unique second column
    for i in range(1, df.shape[1]):
        candidate_col = df.iloc[:, i]
        
        # Ignore the first 3 rows when checking for uniqueness
        if not first_col.equals(candidate_col):
            selected_columns.append(candidate_col)
            break

    # If we couldn't find a second unique column, raise an error
    if len(selected_columns) >= 2:
        # Create new DataFrame with selected columns
        return pd.DataFrame({"Col1": selected_columns[0], "Col2": selected_columns[1]})

    else:
        return None


for table in doc.tables:
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])  # Extract text from each cell

    df = pd.DataFrame(data)

    new_df = get_first_two_unique_columns(df, i)

    if new_df is None:
        None
        
    else:

        new_df.columns = ['PREFERRED AGENTS', 'NON-PREFERRED AGENTS']
    
        same_value_rows = new_df[new_df.apply(lambda x: x.nunique() == 1, axis=1)]
        df_filtered = new_df.drop(same_value_rows.index).reset_index(drop=True)
    
        try:
            preferred_agents = df_filtered["PREFERRED AGENTS"].astype(str).str.split("\n").explode().tolist()
        except KeyError:
            preferred_agents = []
        
        prior_auth_agents = df_filtered["NON-PREFERRED AGENTS"].astype(str).str.split("\n").explode().tolist()
    
        max_length = max(len(preferred_agents), len(prior_auth_agents))
        preferred_agents += [None] * (max_length - len(preferred_agents))
        prior_auth_agents += [None] * (max_length - len(prior_auth_agents))
        
        new_data = {
            "Preferred": preferred_agents,
            "Non-Preferred": prior_auth_agents
        }
        new_df = pd.DataFrame(new_data)
    
        all_tables.append(new_df)
    
        i += 1

final_df = pd.concat(all_tables)

final_df.to_csv('../CO_PDL.csv', index=False)