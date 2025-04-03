import pandas as pd
import os
import sys
from utils import resource_path


def get_base_dir():
    if getattr(sys, 'frozen', False):
        # When bundled with PyInstaller, the executable’s directory is used.
        return os.path.dirname(sys.executable)
    else:
        # When running as a script, use the directory of the script.
        return os.path.dirname(os.path.abspath(__file__))

class DataManager:
    def __init__(self, state):
        self.state = state
        self.pdl_df = pd.read_csv(resource_path(f'{state}/{state}_PDL.csv'))
        self.capsule_df = pd.read_csv(resource_path('drugs.csv'))
        self.state_data = pd.read_csv(resource_path(f'{state}/{state}_data.csv'))
        self.in_data = []
        self.not_in_data = []
        self.statuses = []
        self.skipped_drugs = []
        
    def build_initial_data(self):
        # Iterate over capsule drugs and build lists of drugs already in state_data versus those that are not
        for drug in self.capsule_df.Drugs:
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
                # If the pdl_name isn’t found in the PDL dataframe, add to not_in_data for manual processing
                self.not_in_data.append(entry['capsule_name'])
                
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
        skipped_df = pd.DataFrame(self.skipped_drugs)

        base_dir = get_base_dir()  # Use the base directory of the executable or script
        output_dir = os.path.join(base_dir, self.state)
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        # Save state data
        output_path = os.path.join(output_dir, f'{self.state}_data.csv')
        self.state_data.to_csv(output_path, index=False)

        # Save output data
        output_path = os.path.join(output_dir, f'{self.state}_output_data.csv')
        output_df.to_csv(output_path, index=False)

        # Save skipped data
        output_path = os.path.join(output_dir, f'{self.state}_skipped_data.csv')
        skipped_df.to_csv(output_path, index=False)

        print("Dataframes saved successfully.")