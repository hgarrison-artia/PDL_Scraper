import pandas as pd
import tabula

file = 'DE_PDL.pdf'

df = tabula.read_pdf(file, pages='all')

print(df)
