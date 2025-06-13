from docx import Document
from lxml import etree
from zipfile import ZipFile
import pandas as pd

def get_table_class_map_combined(docx_path):
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
    main_header = None
    sub_header = None

    # Define known subheader patterns (expand as needed)
    subheader_keywords = [
        "VERY HIGH POTENCY", "HIGH POTENCY", "MEDIUM POTENCY", "LOW POTENCY",
        "RAPID ACTING", "SHORT ACTING", "INTERMEDIATE ACTING", "LONG ACTING", "PREMIXED COMBINATIONS"
    ]

    for child in children:
        if child.tag.endswith('p'):
            drawing = child.xpath(".//w:drawing", namespaces=ns)
            pict = child.xpath(".//w:pict", namespaces=ns)
            if drawing or pict:
                texts = child.xpath(".//w:t", namespaces=ns)
                text = "".join([t.text for t in texts if t.text])
                if text:
                    # Clean up the text: remove 'TABLE OF CONTENTS', special chars, and normalize spaces
                    text = text.replace('TABLE OF CONTENTS', '').strip()
                    # Remove any non-alphanumeric/non-dash characters (like ***5, etc.)
                    text = ''.join([c for c in text if c.isalnum() or c.isspace() or c in '–-']).strip()
                    # Normalize multiple spaces to single space
                    text = ' '.join(text.split())

                    # Robust duplication check: check for exact half-string repetition
                    if len(text) % 2 == 0: # Only if length is even
                        half_len = len(text) // 2
                        if text[:half_len] == text[half_len:]:
                            text = text[:half_len]

                    # Finally, split by '***' (if still present after deduplication)
                    text = text.split('***')[0].strip()

                    # Heuristic: if text is in subheader_keywords, treat as subheader
                    if text.upper() in subheader_keywords:
                        sub_header = text
                    # If text is all uppercase or contains a dash, treat as main header
                    elif text.isupper() or " – " in text or " - " in text:
                        main_header = text
                        sub_header = None  # Reset subheader when a new main header is found
        elif child.tag.endswith('tbl'):
            if main_header and sub_header:
                table_class_map.append(f"{main_header}: {sub_header}")
            elif main_header:
                table_class_map.append(main_header)
            else:
                table_class_map.append(None)
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
table_class_map = get_table_class_map_combined(docx_file)
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
    final_df = final_df[~final_df['pdl_name'].str.contains('Trial and failure', case=False, na=False)].reset_index(drop=True)
    final_df.to_csv('NH_PDL.csv', index=False)
else:
    print("No data was collected. Check if tables and textboxes are being found correctly.")