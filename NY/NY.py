import pdfplumber
import pandas as pd
import re

def clean_text(text):
    # Remove superscripts and special marks
    # Remove ™, ®, and F/Q/D (with or without spaces or slashes)
    text = re.sub(r"[™®]", "", text)
    text = re.sub(r"\bF\s*/\s*Q\s*/\s*D\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)  # Collapse multiple spaces
    return text.strip()

preferred_list = []
non_preferred_list = []

# x-coordinates of Preferred drugs, Non-Preferred drugs, and Indentation
preferred_min = 37.44
non_preferred_min = 221.78
indent_x0 = 7.2
error_bound = 0.05

def is_exact_x(x, target, bound):
    return abs(x - target) <= bound

def process_text_line(line):
    if not line:
        return None, None, False
    x0 = line['x0']
    text = clean_text(line['text'].strip())  # Clean and remove trailing/leading blank characters
    # Indented line: concatenate to current entry only if we have a valid entry
    if is_exact_x(x0, preferred_min + indent_x0, error_bound):
        return text, 'Preferred', 'indent'
    elif is_exact_x(x0, non_preferred_min + indent_x0, error_bound):
        return text, 'Non-Preferred', 'indent'
    # New Preferred entry: only if x0 matches preferred_min
    elif is_exact_x(x0, preferred_min, error_bound):
        return text, 'Preferred', 'new'
    # New Non-Preferred entry: only if x0 matches non_preferred_min
    elif is_exact_x(x0, non_preferred_min, error_bound):
        return text, 'Non-Preferred', 'new'
    # Otherwise, ignore this line
    return None, None, False

pdl_entries = []
current_entry = ""
current_status = ""

with pdfplumber.open("NY.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        lines = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
        for line in lines:
            text, status, kind = process_text_line(line)
            if kind == 'new':
                if current_entry:
                    pdl_entries.append([current_entry.strip(), current_status])
                current_entry = text
                current_status = status
            elif kind == 'indent' and current_entry:
                current_entry += " " + text
            else:
                # If line is ignored and we have a current entry, save and reset
                if current_entry:
                    pdl_entries.append([current_entry.strip(), current_status])
                    current_entry = ""
                    current_status = ""
        if current_entry:
            pdl_entries.append([current_entry.strip(), current_status])
            current_entry = ""
            current_status = ""

df = pd.DataFrame(pdl_entries, columns=["pdl_name", "status"])
df.to_csv("NY_PDL.csv", index=False)

# import os
# import layoutparser as lp
# from pdf2image import convert_from_path
# import cv2

# output_dir = "pages"
# os.makedirs(output_dir, exist_ok=True)

# try:
#     pages = convert_from_path("NY.pdf", dpi=300, poppler_path="/opt/homebrew/bin")
#     for i, page in enumerate(pages):
#         img_path = os.path.join(output_dir, f'page_{i}.png')
#         page.save(img_path, 'PNG')
#         print(f"Saved: {img_path}")
#         # Optional: Read with cv2
#         # image = cv2.imread(img_path)
# except Exception as e:
#     print(f"Error: {e}")
