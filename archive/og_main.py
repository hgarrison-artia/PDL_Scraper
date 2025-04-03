import pandas as pd
import tkinter as tk
from tkinter import Listbox, Button

#state = input('Choose a state (e.g., AK) ')
state = 'AK'

pdl_df = pd.read_csv(f'{state}/{state}_PDL.csv')
capsule_df = pd.read_csv('drugs.csv')
state_data = pd.read_csv(f'{state}/{state}_data.csv')

in_data = []
not_in_data = []

for drug in capsule_df.Drugs:
    if drug in list(state_data['capsule_name']):
        subset = state_data.loc[state_data['capsule_name'] == drug]
        for _, row in subset.iterrows():
            in_data.append({'therapeutic_class': row.iloc[0],
                            'capsule_name': row.iloc[1],
                            'pdl_name': row.iloc[2]})
    else:
        not_in_data.append(drug)
        
statuses = []
skipped_drugs = []

for entry in in_data:
    if entry['pdl_name'] in list(pdl_df['pdl_name']):
        status = pdl_df.loc[pdl_df['pdl_name'] == entry['pdl_name'], 'status'].unique()
        if len(status) > 1:
            print(f"{entry['pdl_name']} listed on PDL with multiple different PDL statuses!!!")
            quit
        if 'Preferred' in status:
            statuses.append({'therapeutic_class': entry['therapeutic_class'],
                             'capsule_name': entry['capsule_name'],
                             'pdl_name': entry['pdl_name'],
                             'status': 'Preferred'})
        else:
            statuses.append({'therapeutic_class': entry['therapeutic_class'],
                             'capsule_name': entry['capsule_name'],
                             'pdl_name': entry['pdl_name'],
                             'status': 'Non-Preferred'})
    else:
        not_in_data.append(entry['capsule_name'])

skipped_df = pd.DataFrame(columns=['capsule_name'])
output_df = pd.DataFrame(statuses)

def select_drug(drug_index):
    global skipped_df
    first_word = drug.split()[0].lower()
    matches = pdl_df[pdl_df['pdl_name'].str.lower().str.contains(first_word, na=False)]
    
    # Auto-skip if no matches found
    if matches.empty:
        skipped_drugs.append({'capsule_name': drug})
        process_next(drug_index + 1)
        return
    
    def save_selection():
        selected_index = listbox.curselection()
        if selected_index:
            selected_text = listbox.get(selected_index[0])
            selected_drug = selected_text.split(" | ")[0]  # Extract just the pdl_name
            selected_row = pdl_df.loc[pdl_df['pdl_name'] == selected_drug].iloc[0]
            
            # Save to output_df
            statuses.append({'therapeutic_class': selected_row['therapeutic_class'],
                             'capsule_name': drug,
                             'pdl_name': selected_row['pdl_name'],
                             'status': selected_row['status']})
            
            # Save to state_data
            state_data.loc[len(state_data)] = {
                'therapeutic_class': selected_row['therapeutic_class'],
                'capsule_name': drug,
                'pdl_name': selected_row['pdl_name']
            }
            
        root.destroy()
        process_next(drug_index + 1)
    
    def skip():
        skipped_drugs.append({'capsule_name': drug})
        root.destroy()
        process_next(drug_index + 1)
    
    def exit_program():
        root.destroy()
        save_dataframes()
    
    root = tk.Tk()
    root.title(f"Select match for {drug}")
    
    tk.Label(root, text=f"Select a match for: {drug}").pack()
    listbox = Listbox(root, width=80, height=10)
    listbox.pack()
    
    for _, row in matches.iterrows():
        listbox.insert(tk.END, f"{row['pdl_name']} | {row['therapeutic_class']} | {row['status']}")
    
    btn_save = Button(root, text="Save", command=save_selection)
    btn_save.pack()
    
    btn_skip = Button(root, text="Skip", command=skip)
    btn_skip.pack()
    
    btn_exit = Button(root, text="Exit and Save", command=exit_program)
    btn_exit.pack()
    
    root.mainloop()

def process_next(index):
    if index < len(not_in_data):
        global drug
        drug = not_in_data[index]
        select_drug(index)
    else:
        global skipped_df
        skipped_df = pd.DataFrame(skipped_drugs)
        save_dataframes()

def save_dataframes():
    global statuses, skipped_drugs
    skipped_df = pd.DataFrame(skipped_drugs)
    output_df = pd.DataFrame(statuses)
    output_df.to_csv(f'{state}/{state}_output_data.csv', index=False)
    skipped_df.to_csv(f'{state}/{state}_skipped_data.csv', index=False)
    state_data.to_csv(f'{state}/{state}_data.csv', index=False)
    print("Dataframes saved successfully.")

if not_in_data:
    process_next(0)


output_df = pd.DataFrame(statuses)
output_df[['therapeutic_class', 'capsule_name', 'pdl_name']].to_csv(f'{state}/{state}_data.csv', index=False)

# output_df.to_csv(f'{state}/{state}_output.csv')
# skipped_df.to_csv(f'{state}/{state}_skipped.csv')
