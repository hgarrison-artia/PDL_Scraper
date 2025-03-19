import openpyxl
import csv

file_path = "IA.xlsx"
wb = openpyxl.load_workbook(file_path)
ws = wb.active

# Unmerge all merged cells
for merged_range in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(merged_range))

# Keywords to identify the header row
header_keywords = {key.strip() for key in ["B, G or O", "P, N, R or NR", "Therapeutic Category", "PA Form Link"]}

# Find the row index where the headers appear
header_row = None
column_indices = {}

# Find the header row and identify column indices for the relevant headers
for idx, row in enumerate(ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True), start=1):
    # Strip spaces from non-empty cells and check for header keywords
    cleaned_row = [cell.strip() if isinstance(cell, str) else cell for cell in row]
    
    if any(cell in header_keywords for cell in cleaned_row if cell):  # Ignore empty cells
        header_row = idx
        # Identify column indices, ensuring they aren't empty
        for col_idx, cell in enumerate(cleaned_row, start=1):
            if cell in header_keywords:
                column_indices[cell] = col_idx
        break  # Stop once we find the first valid header row


if not header_row or not column_indices:
    raise ValueError("Header row not found or required columns are missing. Please check the file structure.")

# Define the output CSV column headers
column_headers = ["Drug Name", "Preferred, Non-Preferred, Reviewed, Non-Reviewed"]

# Initialize data list
data = [column_headers]
last_category = None  # To track the last seen Therapeutic Category

# Validation functions
def validate_text(value):
    return isinstance(value, str) and bool(value.strip())  # Ensure it's a non-empty string

def validate_pnrnr(value):
    return value in ["P", "N", "R", "NR"]

# Extract data from the relevant columns based on dynamic header detection
for row in ws.iter_rows(min_row=header_row + 1, values_only=True):

    # Check if the row is a repeated header and skip it
    if any(cell in header_keywords for cell in row if cell):
        continue  # Skip repeated headers

    # Extract relevant columns
    extracted_row = [
        row[column_indices.get("Therapeutic Category", None) - 1] if "Therapeutic Category" in column_indices else None,
        row[column_indices.get("P, N, R or NR", None) - 1] if "P, N, R or NR" in column_indices else None,
    ]

    # Skip rows where all extracted values are empty
    if all(value is None or value == "" for value in extracted_row):
        continue  # Skip this row
    
    # Validate Drug Name (Therapeutic Category)
    if extracted_row[0] and not validate_text(extracted_row[0]):
        extracted_row[0] = "Error"

    # Validate Preferred, Non-Preferred, Reviewed, Non-Reviewed
    if extracted_row[1] and not validate_pnrnr(extracted_row[1]):
        extracted_row[1] = "Error"

    data.append(extracted_row)

# Export data to CSV
csv_file_path = "../IA_PDL.csv" 
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Data successfully exported to {csv_file_path}")

