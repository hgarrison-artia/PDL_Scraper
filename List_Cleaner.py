import pandas as pd
import openpyxl

state = input("Choose a State")

# Load workbook and sheet
wb = openpyxl.load_workbook(f"{state}/{state}_output_data.xlsx")
ws = wb.active

# Find yellow rows (Excel yellow is usually 'FFFFFF00' or 'FFFF00')
yellow_rows = set()
for row in ws.iter_rows(min_row=2):
    for cell in row:
        fill = cell.fill
        if fill and fill.fill_type == 'solid':
            color = fill.start_color.rgb
            if color is not None and color.upper() in ['FFFFFF00', 'FFFF00']:
                yellow_rows.add(cell.row)
                break

df = pd.read_excel(f"{state}/{state}_output_data.xlsx")

# Remove yellow-highlighted rows 
df_clean = df.drop([i-2 for i in yellow_rows], axis=0).reset_index(drop=True)
print(df_clean)

#Check to make sure number of rows removed is correct 
count = len(yellow_rows)
print(count)

df_clean.to_csv(f"{state}/{state}_Data_Cleaned.csv", index=False)