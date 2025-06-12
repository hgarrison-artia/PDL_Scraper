from docx import Document
from lxml import etree
from zipfile import ZipFile
import pandas as pd

def get_table_class_map(docx_path):
    with ZipFile(docx_path) as docx_zip:
        xml_content = docx_zip.read("word/document.xml")
    tree = etree.fromstring(xml_content)
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
        "v": "urn:schemas-microsoft-com:vml",
        "o": "urn:schemas-microsoft-com:office:office"
    }
    body = tree.find(".//w:body", namespaces=ns)
    children = list(body)
    table_class_map = []
    current_class = None
    for child in children:
        # Check for textbox in paragraph
        if child.tag.endswith('p'):
            drawing = child.xpath(".//w:drawing", namespaces=ns)
            pict = child.xpath(".//w:pict", namespaces=ns)
            if drawing or pict:
                texts = child.xpath(".//w:t", namespaces=ns)
                text = "".join([t.text for t in texts if t.text])
                # Clean up the text
                if text:
                    text = text.replace('TABLE OF CONTENTS', '')
                    text = ''.join([c for c in text if not c.isdigit() and c != '*'])
                    text = text.split('***')[0].strip()
                    # Remove duplicated text (e.g., "FOOBARFOOBAR" -> "FOOBAR")
                    half = len(text) // 2
                    if half > 0 and text[:half] == text[half:]:
                        text = text[:half]
                    # Remove subcategories and known non-class text
                    skip = [
                        'RAPID ACTING', 'SHORT ACTING', 'INTERMEDIATE ACTING', 'LONG ACTING', 'PREMIXED COMBINATIONS',
                        'ORAL', 'RECTAL', 'VERY HIGH POTENCY', 'HIGH POTENCY', 'MEDIUM POTENCY', 'LOW POTENCY',
                        'RIBAVIRIN PRODUCTS', 'DIRECT ACTING ANTIVIRAL PRODUCTS', 'BUPRENORPHINE – CONTAINING ORAL',
                        'BUPRENORPHINE – CONTAINING INJECTABLE', 'OPIOID REVERSAL AGENTS', 'OTHER', 'DISEASE MODIFYING THERAPY'
                    ]
                    if text and text not in skip:
                        current_class = text
        # Check for table
        elif child.tag.endswith('tbl'):
            table_class_map.append(current_class)
    return table_class_map

def get_tables(docx_path):
    doc = Document(docx_path)
    all_data = []
    for table in doc.tables:
        data = []
        for row in table.rows:
            data.append([cell.text for cell in row.cells])
        df = pd.DataFrame(data)
        if not df.empty and len(df.columns) > 0:
            df.columns = df.iloc[0]
            df = df.iloc[1:]
            all_data.append(df)
    return all_data

docx_file = "NH.docx"
table_class_map = get_table_class_map(docx_file)
all_data = get_tables(docx_file)

all_temps = []
for table_idx, table in enumerate(all_data):
    tc = table_class_map[table_idx] if table_idx < len(table_class_map) else None
    if tc is None:
        continue
    cols = table.columns
    status = []
    pdl_name = []
    therapeutic_class = []
    for index, row in table.iterrows():
        try:
            prefs = row[cols[0]].split('\n')
            for i in prefs:
                if i.strip():
                    pdl_name.append(i.strip())
                    status.append('Preferred')
                    therapeutic_class.append(tc)
        except:
            None
        try:
            nonprefs = row[cols[1]].split('\n')
            for i in nonprefs:
                if i.strip():
                    pdl_name.append(i.strip())
                    status.append('Non-Preferred')
                    therapeutic_class.append(tc)
        except:
            None
    if pdl_name:
        temp_df = pd.DataFrame([therapeutic_class, pdl_name, status]).transpose()
        temp_df.columns = ['therapeutic_class', 'pdl_name', 'status']
        all_temps.append(temp_df)

if all_temps:
    final_df = pd.concat(all_temps).reset_index(drop=True)
    final_df['pdl_name'] = [name.replace('*', '') for name in final_df['pdl_name']]
    # Remove rows where pdl_name contains 'Trial and failure'
    final_df = final_df[~final_df['pdl_name'].str.contains('Trial and failure', case=False, na=False)].reset_index(drop=True)
    final_df.to_csv('NH_PDL.csv', index=False)
else:
    print("No data was collected. Check if tables and textboxes are being found correctly.")