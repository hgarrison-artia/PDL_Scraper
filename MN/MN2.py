import xml.etree.ElementTree as ET

# load and find your Document element
tree = ET.parse('MN.xml')
root = tree.getroot()
doc = root.find('.//Document')   # or use findall()[1] as before

all_tables = doc.findall('.//Table')
for ti, table in enumerate(all_tables, 1):
    # 1) grab column names from the <THead>
    headers = [th.text.strip() for th in table.findall('.//THead/TH')]
    print(f"\nTable {ti} — columns:", headers)

    # 2) iterate each row in the <TBody>
    for row in table.findall('.//TBody/TR'):
        cells = [td.text.strip() if td.text else '' for td in row.findall('TD')]
        # now you have a list of strings matching headers
        record = dict(zip(headers, cells))
        print(record)
