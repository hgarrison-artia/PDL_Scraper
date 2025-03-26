import openpyxl
import csv

file_path = "IL.xlsx" 
wb = openpyxl.load_workbook(file_path)
ws = wb.active

# Unmerge all merged cells
for merged_range in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(merged_range))

# Keywords to identify the header row
header_keywords = {"Drug Class", "Drug Name", "Dosage Form", "Preferred", "Preferred With PA", "Non-Preferred"}

# Find the row index where the headers appear
header_row = None
column_indices = {}

# Find the header row and identify column indices for the relevant headers
for idx, row in enumerate(ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True), start=1):
    if row and any(cell in header_keywords for cell in row if cell):  # Ignore empty cells
        header_row = idx
        # Identify the column index of each required header
        for col_idx, cell in enumerate(row, start=1):
            if cell in header_keywords:
                column_indices[cell] = col_idx
        break

if not header_row or not column_indices:
    raise ValueError("Header row not found or required columns are missing. Please check the file structure.")

# Define the output CSV column headers
column_headers = ["Therapeutic Class", "Drug Name", "Dosage Form", "Status"]

# Initialize data list
data = [column_headers]

# Validation functions
def validate_text(value):
    return isinstance(value, str) and bool(value.strip())  # Ensure it's a non-empty string

last_category = None  # To track the last seen Therapeutic Category

# Extract data from the relevant columns based on dynamic header detection
for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
    # Extract the relevant columns based on the header
    drug_class_idx = column_indices.get("Drug Class")
    drug_name_idx = column_indices.get("Drug Name")
    dosage_form_idx = column_indices.get("Dosage Form")
    preferred_idx = column_indices.get("Preferred")
    preferred_with_pa_idx = column_indices.get("Preferred With PA")
    non_preferred_idx = column_indices.get("Non-Preferred")

    therapeutic_class = row[drug_class_idx - 1] if drug_class_idx and row[drug_class_idx - 1] else None
    if therapeutic_class:
        last_category = therapeutic_class
    else:
        therapeutic_class = last_category

    extracted_row = [
        therapeutic_class,
        row[drug_name_idx - 1] if drug_name_idx else None,
        row[dosage_form_idx - 1] if dosage_form_idx else None,
        # Concatenate the "Preferred", "Preferred With PA", and "Non-Preferred" column values
        f"{row[preferred_idx - 1] if preferred_idx else ''} {row[preferred_with_pa_idx - 1] if preferred_with_pa_idx else ''} {row[non_preferred_idx - 1] if non_preferred_idx else ''}".strip()
    ]
    
    # Validate each column before assigning
    for i in range(len(extracted_row)):
        if extracted_row[i] is not None and not validate_text(extracted_row[i]):
            extracted_row[i] = "Error"
        elif extracted_row[i] is None:
            extracted_row[i] = "Error"

    data.append(extracted_row)

# Export data to CSV
csv_file_path = "IL_PDL.csv" 
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Data successfully exported to {csv_file_path}")
