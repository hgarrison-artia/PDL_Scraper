import pdfplumber
import pandas as pd

file_path = 'MT.pdf'

all_tables = []

with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table)
            all_tables.append(df)

table_nums = []
p_agents = []
np_agents = []
np_agents2 = []

table_num = 0

for table in all_tables:
    for index, row in table.iterrows():
        table_nums.append(table_num)
        p_agents.append(table[0][index])
        np_agents.append(table[1][index])
        np_agents2.append(table[2][index])
    table_num += 1

df = pd.DataFrame([table_nums, p_agents, np_agents, np_agents2]).transpose()
df.columns = ['table_num', 'Preferred Agents', 'Non-Preferred', 'Non-Preferred Cont.']
df = df[df['Preferred Agents'] != 'Preferred Agents']

df = df.melt(id_vars='table_num', value_name='Products', var_name='Status')
df = df[df['Products']!=''].reset_index(drop=True)
df = df[~df['Products'].isna()].reset_index(drop=True)

# Conservative heuristic to join continued lines

def join_continued_lines(cell):
    if pd.isna(cell):
        return cell
    lines = cell.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if new_lines:
            prev = new_lines[-1]
            # Only join if previous line ends with a comma or open parenthesis and current line starts with lowercase or '('
            if (prev.rstrip().endswith((',', '(')) and (stripped[0].islower() or stripped.startswith('('))):
                new_lines[-1] += ' ' + stripped
                continue
        new_lines.append(stripped)
    return '\n'.join(new_lines)

df['Products'] = df['Products'].apply(join_continued_lines)
df = df.assign(Products=df['Products'].str.split('\n')).explode('Products')
df = df[df['Products'] != ''].reset_index(drop=True)

print(df[df['table_num']==0])