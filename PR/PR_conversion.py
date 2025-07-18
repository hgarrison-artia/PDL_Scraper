import os
from pdf2docx import Converter

pdf_dir = 'PDLs_pdf'
docx_dir = 'PDLs_docx_converted'
os.makedirs(docx_dir, exist_ok=True)

# Convert PDFs to DOCX
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, filename)
        docx_filename = os.path.splitext(filename)[0] + '.docx'
        docx_path = os.path.join(docx_dir, docx_filename)
        print(f'Converting {pdf_path} to {docx_path}...')
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
print('All conversions done.')