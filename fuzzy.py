import pandas as pd
from thefuzz import fuzz
from fuzzywuzzy import process


def fuzzy_lookup(drugs, statuses, pdl_date, state_input):
    statuses['Preferred'] = statuses['Preferred'].str.replace(r'\s*\(.*?\)', '', regex=True)
    statuses['Non-Preferred'] = statuses['Non-Preferred'].str.replace(r'\s*\(.*?\)', '', regex=True)

    final_drugs = []
    final_pdl_drugs = []
    final_statuses = []
    final_scores = []

    for drug in drugs['Drugs']:
        result_stats = []
        first_word = drug.split()[0]
        preferred_filtered_df = list(statuses[statuses['Preferred'].str.contains(first_word, case=False, na=False)]['Preferred'])

        for i in range(len(preferred_filtered_df)):
            result_stats.append('P')

        nonpreferred_filtered_df = list(statuses[statuses['Non-Preferred'].str.contains(first_word, case=False, na=False)]['Non-Preferred'])
        for i in range(len(nonpreferred_filtered_df)):
            result_stats.append('NP')   

        test_drugs = preferred_filtered_df
        for i in nonpreferred_filtered_df:
            test_drugs.append(i)

        if len(test_drugs) == 0:
            final_drugs.append(drug)
            final_pdl_drugs.append("Non PDL")
            final_statuses.append("Non PDL")
            final_scores.append("Non PDL")

        else:

            results = pd.DataFrame()
            results['Drugs'] = test_drugs
            results['Statuses'] = result_stats
            pdl_drug = process.extractOne(drug, results['Drugs'], scorer=fuzz.token_sort_ratio)[0]
            score = fuzz.token_sort_ratio(drug, pdl_drug)
            pdl_status = list(results[results['Drugs']==pdl_drug]['Statuses'].astype(str))[0]
            final_drugs.append(drug)
            final_pdl_drugs.append(pdl_drug)
            final_statuses.append(pdl_status)
            final_scores.append(score)
            print(f"Drug: {drug}, PDL Drug: {pdl_drug}, Status: {pdl_status}, Score: {score}")

    final_df = pd.DataFrame()
    final_df['Drugs'] = final_drugs
    final_df['PDL Drugs'] = final_pdl_drugs
    final_df['PDL Statuses'] = final_statuses
    final_df['Score'] = final_scores
    final_df.insert(0, 'State', state_input)
    final_df.insert(1, 'PDL Date', pdl_date)
    

    completed_df = final_df[final_df['Score']==100]
    non_pdl_df = final_df[final_df['Score']=='Non PDL']
    skipped_df = final_df[final_df['Score']!=100]
    skipped_df = skipped_df[skipped_df['Score']!='Non PDL']

    return completed_df, non_pdl_df, skipped_df


drugs = pd.read_csv('drugs.csv')
state_input = input('What state would you like to test? ')
pdl_date = input('What is the effective date of the PDL? (mmddyyyy) ')

statuses = pd.read_csv(f'{state_input}/{state_input}_PDL.csv')

if state_input == 'MS':
    #statuses = pd.read_csv('MS_PDL.csv')
    statuses.columns = ['Preferred', 'Non-Preferred']

elif state_input == 'CO':
    #statuses = pd.read_csv('CO_PDL.csv')
    statuses.columns = ['Preferred', 'Non-Preferred']

elif state_input == 'GA':
    #statuses = pd.read_csv('GA_PDL.csv')

    preferred_drugs = statuses.loc[statuses['Preferred'] == 'P', 'Drug'].reset_index(drop=True)

    non_preferred_drugs = statuses.loc[statuses['Non-Preferred'] == 'NP', 'Drug'].reset_index(drop=True)

    max_len = max(len(preferred_drugs), len(non_preferred_drugs))
    preferred_drugs = preferred_drugs.reindex(range(max_len))
    non_preferred_drugs = non_preferred_drugs.reindex(range(max_len))

    statuses = pd.DataFrame({
        'Preferred': preferred_drugs,
        'Non-Preferred': non_preferred_drugs
    })

elif state_input == 'AK':
    #statuses = pd.read_csv('AK_PDL.csv')

    preferred_drugs = statuses.loc[statuses['PDL Status'] == 'ON', 'Product'].reset_index(drop=True)

    non_preferred_drugs = statuses.loc[statuses['PDL Status'] == 'OFF', 'Product'].reset_index(drop=True)

    max_len = max(len(preferred_drugs), len(non_preferred_drugs))
    preferred_drugs = preferred_drugs.reindex(range(max_len))
    non_preferred_drugs = non_preferred_drugs.reindex(range(max_len))

    statuses = pd.DataFrame({
        'Preferred': preferred_drugs,
        'Non-Preferred': non_preferred_drugs
    })

elif state_input == 'FL':
    # FL has a different structure for the PDL

    #statuses = pd.read_csv('FL_PDL.csv')

    preferred_drugs = statuses.loc[statuses['Generic Name'].notna(), 'Generic Name'].reset_index(drop=True)

    non_preferred_drugs = pd.Series(dtype='object')

    max_len = max(len(preferred_drugs), len(non_preferred_drugs))

    preferred_drugs = preferred_drugs.reindex(range(max_len), fill_value=None)
    non_preferred_drugs = non_preferred_drugs.reindex(range(max_len), fill_value=None)

    statuses = pd.DataFrame({
        'Preferred': preferred_drugs,
        'Non-Preferred': non_preferred_drugs
    })

elif state_input == 'IA':
    #statuses = pd.read_csv('IA_PDL.csv')

    preferred_drugs = statuses.loc[statuses['Preferred, Non-Preferred, Reviewed, Non-Reviewed'] == 'P', 'Drug Name'].reset_index(drop=True)

    non_preferred_drugs = statuses.loc[statuses['Preferred, Non-Preferred, Reviewed, Non-Reviewed'] == 'NP', 'Drug Name'].reset_index(drop=True)

    max_len = max(len(preferred_drugs), len(non_preferred_drugs))
    preferred_drugs = preferred_drugs.reindex(range(max_len))
    non_preferred_drugs = non_preferred_drugs.reindex(range(max_len))

    statuses = pd.DataFrame({
        'Preferred': preferred_drugs,
        'Non-Preferred': non_preferred_drugs
    })

elif state_input == 'IL':
    #statuses = pd.read_csv('IL_PDL.csv')

    preferred_drugs = statuses.loc[(statuses['Status'] == 'PREFERRED') | (statuses['Status'] == 'PREFERRED_WITH_PA'), 'Drug Name'].reset_index(drop=True)

    non_preferred_drugs = statuses.loc[statuses['Status'] == 'NON_PREFERRED', 'Drug Name'].reset_index(drop=True)

    max_len = max(len(preferred_drugs), len(non_preferred_drugs))
    preferred_drugs = preferred_drugs.reindex(range(max_len))
    non_preferred_drugs = non_preferred_drugs.reindex(range(max_len))

    statuses = pd.DataFrame({
        'Preferred': preferred_drugs,
        'Non-Preferred': non_preferred_drugs
    })

completed_df, non_pdl_df, skipped_df = fuzzy_lookup(drugs, statuses, pdl_date, state_input)

completed_df.to_excel(f'{state_input}/{state_input}_completed_output.xlsx', index=False)
non_pdl_df.to_excel(f'{state_input}/{state_input}_non_pdl_output.xlsx', index=False)
skipped_df.to_excel(f'{state_input}/{state_input}_skipped_output.xlsx', index=False)
