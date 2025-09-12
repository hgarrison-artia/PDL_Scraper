import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import numpy as np

username = "artia_readonly"
password = 'ap3ljax#!0frack'
host = "artia-dashboard-psql.postgres.database.azure.com"
port = "5432"              
database = "artia_dashboard"

url = URL.create(
    "postgresql+psycopg2",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database,
)

engine = create_engine(url)

with open('coverage_data.sql', 'r') as f:
    sql_query = f.read()


pdl_status_map = {
    '1': 'Preferred',
    '2': 'Non-Preferred',
    '3': 'Non-PDL',
    '4': 'No State PDL',
    '5': 'Preferred (Not Listed)',
    '6': 'Non-Preferred (Not Listed)',
    '7': 'Blank'
}
    
df = pd.read_sql(sql_query, engine)
drug_df = df
drug_df['capsule_name'] = [product + ' ' + tag if tag != '' else product for product, tag in zip(drug_df['Product'], drug_df['Coverage Tag(s)'])]
drug_df = drug_df.drop_duplicates().reset_index(drop=True)
drug_df = drug_df[['id','ST', 'Product', 'Coverage Tag(s)', 'capsule_name', 'Class', 'PDL Status', 'PDL Status Date']]
drug_df = drug_df.sort_values('id').reset_index(drop=True)
drug_df['PDL Status'] = drug_df['PDL Status'].replace(np.nan,7)
drug_df['PDL Status'] = drug_df['PDL Status'].replace(np.inf,8)
drug_df['PDL Status'] = drug_df['PDL Status'].astype(int).astype(str)
drug_df['PDL Status'] = drug_df['PDL Status'].map(pdl_status_map)
drug_df['PDL Status Date'] = drug_df['PDL Status Date'].astype(str)

nopdl_error = drug_df[(drug_df['PDL Status'] == 'No State PDL') & (drug_df['ST'].isin(['ID', 'RI']))]
nopdl_error.to_csv('No_State_PDL_Errors.csv', index=False)

state = input('Enter State Abbreviation (e.g., GA) ')
pdl_date = input('Enter PDL Effective Date(e.g., 2025-09-01; YYYY-MM-DD) ')

drug_df_refined = drug_df[(drug_df["ST"]==state) & (drug_df['PDL Status Date']==pdl_date)].reset_index(drop=True)
drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Cytokine and CAM Antagonists']

drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Immunomodulators Asthma']
drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Immunomodulators Atopic Dermatitis']
drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Immunomodulators SLE']
drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Immunomodulators Type 1 Diabetes']
drug_df_refined = drug_df_refined[drug_df_refined['Class']!='Ophthalmics Antiinflammatory Immunomodulator'].reset_index(drop=True)

scraper_data = pd.read_csv(f'{state}/{state}_clinical_output_data.csv')
scraper_status_map = scraper_data.set_index('capsule_name')['status'].to_dict()
drug_df_refined['Scraper Status'] = drug_df_refined['capsule_name'].map(scraper_status_map)

pref_pref =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred')) & (drug_df_refined['Scraper Status'].eq('Preferred'))]
pref_nonpref = drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred')) & (drug_df_refined['Scraper Status'].eq('Non-Preferred'))]
pref_nonpdl =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred')) & (drug_df_refined['Scraper Status'].isna())]

nonpref_pref =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred')) & (drug_df_refined['Scraper Status'].eq('Preferred'))]
nonpref_nonpref = drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred')) & (drug_df_refined['Scraper Status'].eq('Non-Preferred'))]
nonpref_nonpdl =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred')) & (drug_df_refined['Scraper Status'].isna())]

nonprefnl_pref =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].eq('Preferred'))]
nonprefnl_nonpref = drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].eq('Non-Preferred'))]
nonprefnl_nonpdl =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].isna())]

prefnl_pref =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].eq('Preferred'))]
prefnl_nonpref = drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].eq('Non-Preferred'))]
prefnl_nonpdl =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Preferred (Not Listed)')) & (drug_df_refined['Scraper Status'].isna())]

nonpdl_pref =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-PDL')) & (drug_df_refined['Scraper Status'].eq('Preferred'))]
nonpdl_nonpref = drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-PDL')) & (drug_df_refined['Scraper Status'].eq('Non-Preferred'))]
nonpdl_nonpdl =  drug_df_refined.loc[(drug_df_refined['PDL Status'].eq('Non-PDL')) & (drug_df_refined['Scraper Status'].isna())]

accuracy_matrix = pd.DataFrame()
accuracy_matrix['Capsule Preferred'] = [len(pref_pref),len(pref_nonpref),len(pref_nonpdl)]
accuracy_matrix['Capsule Non-Preferred'] = [len(nonpref_pref),len(nonpref_nonpref),len(nonpref_nonpdl)]
accuracy_matrix['Capsule NP-NL'] = [len(nonprefnl_pref),len(nonprefnl_nonpref),len(nonprefnl_nonpdl)]
accuracy_matrix['Capsule P-NL'] = [len(prefnl_pref),len(prefnl_nonpref),len(prefnl_nonpdl)]
accuracy_matrix['Capsule Non-PDL'] = [len(nonpdl_pref),len(nonpdl_nonpref),len(nonpdl_nonpdl)]
accuracy_matrix.index = ['PDL Scraper P', 'PDL Scraper NP', 'PDL Scraper Non-PDL']
print('\n\n')
print(accuracy_matrix)

audit_log = pd.concat([pref_nonpref,pref_nonpdl,nonpref_pref,nonpref_nonpdl,nonprefnl_pref,nonprefnl_nonpref,nonpdl_pref,nonpdl_nonpref]).reset_index(drop=True)
audit_log['Notes'] = ''
audit_log['Scraper Status'] = audit_log['Scraper Status'].replace(np.nan,'Not Found by Scraper')
audit_log.to_csv(f'{state}/{state}_audit_log.csv', index=False)