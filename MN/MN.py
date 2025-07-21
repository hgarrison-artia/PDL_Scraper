import xml.etree.ElementTree as ET
import pandas as pd
import re

# Parse the XML file
tree = ET.parse('MN.xml')  # Update this to your actual XML file path
root = tree.getroot()

target = root.find('.//Document[@id="LinkTarget_104"]')

data = []  # To collect rows for the DataFrame

if target is not None:
    h2_tables = []  # List of (H2 text, table) pairs
    current_h2 = None

    # Iterate through all children in order
    for elem in target:
        if elem.tag == 'H2':
            current_h2 = elem
        elif elem.tag == 'Table' and current_h2 is not None:
            h2_tables.append((current_h2, elem))

    # Skip the first H2 as per your instructions
    for h2, table in h2_tables[1:]:
        therapeutic_class = h2.text.strip() if h2.text else ''
        # Find all rows in the table
        rows = table.findall('.//TR')
        for row in rows:
            th = row.find('TH')
            td = row.find('TD')

            # Get all <P> elements in TH (preferred)
            if th is not None:
                preferred = [p.text.strip() for p in th.findall('.//P') if p.text and p.text.strip()]
                for drug in preferred:
                    # Split on 2 or more spaces
                    products = re.split(r' {2,}', drug)
                    for product in products:
                        if product:
                            data.append({
                                'therapeutic_class': therapeutic_class,
                                'pdl_name': product,
                                'status': 'Preferred'
                            })
            # Get all <P> elements in TD (non-preferred)
            if td is not None:
                non_preferred = [p.text.strip() for p in td.findall('.//P') if p.text and p.text.strip()]
                for drug in non_preferred:
                    # Split on 2 or more spaces
                    products = re.split(r' {2,}', drug)
                    for product in products:
                        if product:
                            data.append({
                                'therapeutic_class': therapeutic_class,
                                'pdl_name': product,
                                'status': 'Non-Preferred'
                            })
else:
    print('No <Document> element with id="LinkTarget_104" found.')

# Create DataFrame and print
if data:
    df = pd.DataFrame(data)
    df = df[df['pdl_name']!='Preferred']
    df = df[df['pdl_name']!='Non-Preferred']
    df = df.reset_index(drop=True)
    print(df)
    df.to_csv('MN_PDL.csv', index=False)
else:
    print('No data extracted.')
