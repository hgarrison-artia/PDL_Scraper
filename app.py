import tkinter as tk
from data_manager import DataManager
from gui_selector import DrugSelectorGUI

class DrugMatcherApp:
    def __init__(self, state, process_type):
        self.state = state
        self.process_type = process_type
        self.data_manager = DataManager(state, process_type)
        self.data_manager.build_initial_data()
        self.data_manager.process_existing_data()
        self.current_index = 0
        self.not_in_data = self.data_manager.not_in_data
        # Track history of actual drug pairings for back navigation
        self.pairing_history = []
        # Create one hidden root window
        self.root = tk.Tk()
        self.root.withdraw()

    def start(self):
        # Kick off processing with the first drug
        self.process_next(self.current_index)
        self.root.mainloop()

    def process_next(self, index):
        if index < len(self.not_in_data):
            drug = self.not_in_data[index]
            # Find matches using the first word of the drug name (case-insensitive)
            first_word = drug.split()[0].split('-')[0].split('/')[0].lower()
            matches = self.data_manager.pdl_df[
                self.data_manager.pdl_df['pdl_name'].str.lower().str.contains(first_word, na=False, regex=False)
            ]
            if matches.empty:
                self.data_manager.add_skipped_drug(drug)
                self.current_index += 1
                self.process_next(self.current_index)
            else:
                self.open_gui_for_drug(drug, matches)
        else:
            self.data_manager.save_dataframes()
            self.root.destroy()

    def save_to_all_matching_drugs(self, selected_pdl_name):
        # Get the current drug's first word
        current_drug = self.not_in_data[self.current_index]
        first_word = current_drug.split()[0].split('-')[0].split('/')[0].lower()
        
        # Get the selected PDL drug's details
        selected_row = self.data_manager.pdl_df.loc[
            self.data_manager.pdl_df['pdl_name'] == selected_pdl_name
        ].iloc[0]
        therapeutic_class = selected_row['therapeutic_class']
        status = selected_row['status']
        
        # Find all remaining drugs that start with the same word
        remaining_drugs = []
        for i in range(self.current_index, len(self.not_in_data)):
            drug = self.not_in_data[i]
            if drug.split()[0].split('-')[0].split('/')[0].lower() == first_word:
                remaining_drugs.append(drug)
        
        # Save all matching drugs
        for drug in remaining_drugs:
            self.data_manager.add_status(therapeutic_class, drug, selected_pdl_name, status)
            self.data_manager.update_state_data(therapeutic_class, drug, selected_pdl_name)
            # Add to pairing history
            self.pairing_history.append({
                'drug': drug,
                'pdl_name': selected_pdl_name,
                'therapeutic_class': therapeutic_class,
                'status': status
            })
        
        # Update current index to skip all processed drugs
        self.current_index += len(remaining_drugs)
        self.process_next(self.current_index)

    def open_gui_for_drug(self, drug, matches):
        def save_callback(selected_pdl_name):
            selected_row = self.data_manager.pdl_df.loc[
                self.data_manager.pdl_df['pdl_name'] == selected_pdl_name
            ].iloc[0]
            therapeutic_class = selected_row['therapeutic_class']
            status = selected_row['status']
            self.data_manager.add_status(therapeutic_class, drug, selected_pdl_name, status)
            self.data_manager.update_state_data(therapeutic_class, drug, selected_pdl_name)
            # Add to pairing history
            self.pairing_history.append({
                'drug': drug,
                'pdl_name': selected_pdl_name,
                'therapeutic_class': therapeutic_class,
                'status': status
            })
            self.current_index += 1
            self.process_next(self.current_index)
        
        def skip_callback():
            self.data_manager.add_skipped_drug(drug)
            self.current_index += 1
            self.process_next(self.current_index)
        
        def exit_callback():
            self.data_manager.save_dataframes()
            self.root.destroy()
        
        def back_callback():
            # Undo the last pairing and return to that drug
            if self.pairing_history:
                # Get the last pairing from history
                last_pairing = self.pairing_history.pop()
                
                # Remove the last pairing from state_data and statuses
                self.data_manager.state_data = self.data_manager.state_data[
                    ~((self.data_manager.state_data['capsule_name'] == last_pairing['drug']) & 
                      (self.data_manager.state_data['pdl_name'] == last_pairing['pdl_name']))
                ]
                
                # Remove from statuses
                self.data_manager.statuses = [
                    s for s in self.data_manager.statuses 
                    if not (s['capsule_name'] == last_pairing['drug'] and 
                           s['pdl_name'] == last_pairing['pdl_name'])
                ]
                
                # Find the drug in not_in_data
                if last_pairing['drug'] not in self.not_in_data:
                    self.not_in_data.append(last_pairing['drug'])
                
                # Process the drug again
                self.open_gui_for_drug(
                    last_pairing['drug'],
                    self.data_manager.pdl_df[
                        self.data_manager.pdl_df['pdl_name'].str.lower().str.contains(
                            last_pairing['drug'].split()[0].split('-')[0].split('/')[0].lower(), na=False, regex=False
                        )
                    ]
                )

        def permanent_skip_callback():
            self.data_manager.add_banned_pairings(drug, matches)
            # Remove the current drug from the queue
            if drug in self.not_in_data:
                self.not_in_data.remove(drug)
            # Process the next drug without changing the current index
            self.process_next(self.current_index)

        selector = DrugSelectorGUI(
            self.root,
            drug,
            matches,
            save_callback,
            skip_callback,
            exit_callback,
            back_callback,
            self.current_index,
            len(self.not_in_data),
            self.save_to_all_matching_drugs,
            permanent_skip_callback
        )
        selector.grab_set()  # Makes the window modal
