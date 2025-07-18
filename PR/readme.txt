1. Find PR PDLs from the google drive.  There should be 10 pdf files.
    Find "Formularios de Medicamentos" on the official website. It would lead to the google drive: https://www.ases.pr.gov/proveedores?tab=Farmacias&categoria=Formularios+de+Medicamentos#Farmacia
    Google drive link: https://drive.google.com/drive/folders/12iTCIL8Sfs2uk3Xzz1YzK-JHwS4DYEOW
2. Click "Download all" on the upper right corner and save the zip file.
3. Unzip the file and remove the dates after the PDL names e.g. PDL Dental_20250213.pdf --> PDL Dental.pdf
4. Place the pdf files in the folder under PDL_SCRAPER/PR/PDLs_pdf.
5. Run the code PR_conversion.py first and then PR.py

WS Note: With the 3rd step, I'm hoping that we can replace the old PDLs in the folder more smoothly and prevent any unnecessary duplicate work for the pdf->docx conversion in the code.
         There are two parts of this PR code, one for conversion and another for extraction. It is important that we run both to reflect any changes made.
         It is normal that PR_conversion.py takes ~5 minutes for all the 10 pdfs to be converted.