import pandas as pd
import docx
from docx.oxml.ns import qn

doc = docx.Document('TN.docx')

all_data = []

main_head_hex = '0077C8'
sub_head_hex = 'F2F2F2'

main_head = ''
sub_head = ''

for table in doc.tables:

    
    datas = []
    for row in table.rows:
        data = [cell.text.strip() for cell in row.cells]

        try:
            if row.cells[0]._tc.xpath('.//w:shd')[0].get(qn('w:fill')) == main_head_hex:
                cells = row.cells
                cell_missing = True
                cell_number = 0

                while cell_missing:
                    if cells[cell_number].text.strip() != "":
                        main_head = cells[cell_number].text.strip().split('\n')[0]
                        cell_missing = False
                    else:
                        cell_number += 1

                    if cell_number >= len(cells):
                        cell_missing = False

        except IndexError:
            None

        try:
            if row.cells[0]._tc.xpath('.//w:shd')[0].get(qn('w:fill')) == sub_head_hex:
                cells = row.cells
                cell_missing = True
                cell_number = 0

                while cell_missing:
                    if cells[cell_number].text.strip() != "":
                        sub_head = cells[cell_number].text.strip().split('\n')[0]
                        cell_missing = False
                    else:
                        cell_number += 1

                    if cell_number >= len(cells):
                        cell_missing = False

        except IndexError:
            None


        if sub_head == '':
            tc = ''

        else:
            tc = f'{main_head}: {sub_head}'

        data.insert(0, tc)
        datas.append(data)
        # cell = table.rows[0].cells[0]
        # cell_xml = cell._tc
        # shd = cell_xml.xpath('.//w:shd')
        # fill = shd[0].get(qn('w:fill'))
        # print(fill)

    df = pd.DataFrame(datas)
    # df.columns = ['tc', 'Medication', 'PDL', 'Prior Authorization Criteria', 'Qty. Limits', 'PA Form']

    df = df[df.columns[:3]]

    skipped_indexes = []
    for index, row in df.iterrows():


        # Look for rows with duplicated values in each column
        # Check for All Caps -> Main Class
        # Check for not all Caps & black text merged cell & not italicized & delimited at \n character -> subclass


        if df.iloc[index, 0] == df.columns[0]:
            skipped_indexes.append(index)

        if df.iloc[index, 0] == '':
            skipped_indexes.append(index)

        if df.iloc[index, 1] == '':
            skipped_indexes.append(index)

        if df.iloc[index, 1] == 'Medication':
            skipped_indexes.append(index)
        
        elif df.iloc[index, 1] == df.iloc[index, 2]:
            skipped_indexes.append(index)
    
    if len(skipped_indexes) > 0:
        df.drop(skipped_indexes, inplace=True)

    all_data.append(df.reset_index(drop=True))

tables = []

for table in all_data:
    if table.shape[0] > 0:
        tables.append(table)

for table in tables:
    table.columns = ['therapeutic_class','pdl_name','status']


final_df = pd.concat(tables).reset_index(drop=True)
final_df['status'] = final_df['status'].replace('', 'Missing Status')
final_df['status'] = final_df['status'].replace('P', 'Preferred')
final_df['status'] = final_df['status'].replace('NP', 'Non-Preferred')

final_df['pdl_name'] = [i.replace('®', '') for i in final_df['pdl_name']]
final_df['pdl_name'] = [i.replace('\n', '') for i in final_df['pdl_name']]

final_df.to_csv('TN_PDL.csv', index=False)


