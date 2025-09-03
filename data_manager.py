import pandas as pd
import os

class DataManager:
    def __init__(self, state, process_type):
        self.state = state
        self.process_type = process_type
        self.pdl_df = pd.read_csv(f'{state}/{state}_PDL.csv')
        self.capsule_df = pd.read_csv('drugs.csv')
        # Filter capsule_df to only include drugs for the selected state
        self.capsule_df = self.capsule_df[self.capsule_df['ST'] == state]
        self.state_data = pd.read_csv(f'{state}/{state}_data.csv')
        self.in_data = []
        self.not_in_data = []
        self.statuses = []
        self.skipped_drugs = []
        banned_file = f'{state}/{state}_banned_data.csv'
        if os.path.exists(banned_file):
            self.banned_data = pd.read_csv(banned_file)
        else:
            self.banned_data = pd.DataFrame(columns=['therapeutic_class', 'capsule_name', 'pdl_name'])
        
    def build_initial_data(self):
        # Filter drugs based on process type
        if self.process_type == "Pharmacy":
            # Filter for Cytokine and CAM Antagonists or Immunomodulators
            filtered_drugs = self.capsule_df[
                (self.capsule_df['Class'] == "Cytokine and CAM Antagonists") |
                (self.capsule_df['Class'].str.contains('Immunomodulator', case=False, na=False))
            ]['Drugs']
        else:  # Clinical
            # Filter for drugs NOT in Cytokine and CAM Antagonists or Immunomodulators
            filtered_drugs = self.capsule_df[
                ~((self.capsule_df['Class'] == "Cytokine and CAM Antagonists") |
                  (self.capsule_df['Class'].str.contains('Immunomodulator', case=False, na=False)))
            ]['Drugs']

        # Ensure we only process each drug once even if duplicates exist in drugs.csv
        filtered_drugs = filtered_drugs.drop_duplicates()
        
        print(f"Processing {self.process_type} drugs for {self.state}. Found {len(filtered_drugs)} drugs to process.")
        
        # Iterate over filtered capsule drugs and build lists
        for drug in filtered_drugs:
            if drug in list(self.state_data['capsule_name']):
                subset = self.state_data.loc[self.state_data['capsule_name'] == drug]
                for _, row in subset.iterrows():
                    self.in_data.append({
                        'therapeutic_class': row.iloc[0],
                        'capsule_name': row.iloc[1],
                        'pdl_name': row.iloc[2]
                    })
            else:
                self.not_in_data.append(drug)

        # Remove any drugs that have been permanently skipped
        self.filter_banned_drugs()
                
    def process_existing_data(self):
        # Process drugs already in data to set statuses
        for entry in self.in_data:
            if entry['pdl_name'] in list(self.pdl_df['pdl_name']):
                status_array = self.pdl_df.loc[self.pdl_df['pdl_name'] == entry['pdl_name'], 'status'].unique()
                if len(status_array) > 1:
                    print(f"{entry['pdl_name']} listed on PDL with multiple different PDL statuses!!!")
                    # You may choose to handle this situation differently
                if 'Preferred' in status_array:
                    self.statuses.append({
                        'therapeutic_class': entry['therapeutic_class'],
                        'capsule_name': entry['capsule_name'],
                        'pdl_name': entry['pdl_name'],
                        'status': 'Preferred'
                    })
                else:
                    self.statuses.append({
                        'therapeutic_class': entry['therapeutic_class'],
                        'capsule_name': entry['capsule_name'],
                        'pdl_name': entry['pdl_name'],
                        'status': 'Non-Preferred'
                    })
            else:
                # If the pdl_name isn't found in the PDL dataframe, remove only
                # rows with the same therapeutic_class and pdl_name combination
                # from state_data. Other rows should remain unaffected.
                mask = ~(
                    (self.state_data['therapeutic_class'] == entry['therapeutic_class']) &
                    (self.state_data['pdl_name'] == entry['pdl_name'])
                )
                self.state_data = self.state_data[mask]
                self.not_in_data.append(entry['capsule_name'])

        # Remove any banned drugs that may have been added back
        self.filter_banned_drugs()
                
    def add_status(self, therapeutic_class, capsule_name, pdl_name, status):
        self.statuses.append({
            'therapeutic_class': therapeutic_class,
            'capsule_name': capsule_name,
            'pdl_name': pdl_name,
            'status': status
        })
        
    def add_skipped_drug(self, capsule_name):
        self.skipped_drugs.append({'capsule_name': capsule_name})
        
    def update_state_data(self, therapeutic_class, capsule_name, pdl_name):
        new_row = {
            'therapeutic_class': therapeutic_class,
            'capsule_name': capsule_name,
            'pdl_name': pdl_name
        }
        # Append the new row to the state_data dataframe
        new_row_df = pd.DataFrame([new_row])
        self.state_data = pd.concat([self.state_data, new_row_df], ignore_index=True)
        
    def save_dataframes(self):
        output_df = pd.DataFrame(self.statuses)
        skipped_df = pd.DataFrame(self.skipped_drugs).drop_duplicates()

        banned_filename = f'{self.state}/{self.state}_banned_data.csv'
        if not self.banned_data.empty:
            self.banned_data.drop_duplicates().to_csv(banned_filename, index=False)

        # Save with process type in filename
        output_filename = f'{self.state}/{self.state}_{self.process_type.lower()}_output_data.csv'
        skipped_filename = f'{self.state}/{self.state}_{self.process_type.lower()}_skipped_data.csv'
        
        output_df.sort_values('capsule_name').to_csv(output_filename, index=False, encoding='UTF-8')
        skipped_df.to_csv(skipped_filename, index=False, encoding='UTF-8')
        
        # Only update state_data.csv if there are changes
        if len(self.statuses) > 0:
            self.state_data.sort_values('capsule_name').to_csv(f'{self.state}/{self.state}_data.csv', index=False)
        
        print(f"Dataframes saved successfully for {self.process_type} processing.")

    def filter_banned_drugs(self):
        """Remove any drugs from not_in_data that are listed in banned_data."""
        if not self.banned_data.empty:
            banned_capsules = set(self.banned_data['capsule_name'])
            self.not_in_data = [d for d in self.not_in_data if d not in banned_capsules]
            # Ensure these banned capsules appear in the skipped list
            existing = {d['capsule_name'] for d in self.skipped_drugs}
            for capsule in banned_capsules:
                if capsule not in existing:
                    self.skipped_drugs.append({'capsule_name': capsule})

    def add_banned_pairings(self, capsule_name, matches_df):
        """Record all match options for a capsule drug as permanently skipped."""
        if matches_df is None or matches_df.empty:
            return
        new_rows = matches_df[['therapeutic_class', 'pdl_name']].copy()
        new_rows['capsule_name'] = capsule_name
        self.banned_data = pd.concat([self.banned_data, new_rows], ignore_index=True)
        # Also track the capsule as skipped for this process
        self.add_skipped_drug(capsule_name)

    def remove_last_assignment(self):
        """Remove the last assignment from statuses and state_data, and add the drug back to not_in_data."""
        if self.statuses:
            last_status = self.statuses.pop()
            capsule_name = last_status['capsule_name']
            
            # Remove from state_data
            if not self.state_data.empty:
                self.state_data = self.state_data[
                    ~((self.state_data['capsule_name'] == capsule_name) & 
                      (self.state_data['pdl_name'] == last_status['pdl_name']))
                ]
            
            # Add back to not_in_data if it's not already there
            if capsule_name not in self.not_in_data:
                self.not_in_data.append(capsule_name)
            
            return capsule_name
        return None

    def clear_old_drug_pairings(self):
        """Remove any rows from state_data where capsule_name is not in drugs.csv for the selected state"""
        # Get list of valid drugs from drugs.csv for the selected state
        valid_drugs = set(self.capsule_df['Drugs'].str.lower())
        
        # Filter state_data to keep only rows where capsule_name is in valid_drugs
        self.state_data = self.state_data[
            self.state_data['capsule_name'].str.lower().isin(valid_drugs)
        ]
        
        # Save the updated state_data
        self.state_data.sort_values('capsule_name').to_csv(f'{self.state}/{self.state}_data.csv', index=False)
        print(f"Cleared old drug pairings for {self.state}. Remaining rows: {len(self.state_data)}")
