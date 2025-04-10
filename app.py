import tkinter as tk
from data_manager import DataManager
from gui_selector import DrugSelectorGUI

class DrugMatcherApp:
    def __init__(self, state):
        self.state = state
        self.data_manager = DataManager(state)
        self.data_manager.build_initial_data()
        self.data_manager.process_existing_data()
        self.current_index = 0
        self.not_in_data = self.data_manager.not_in_data
        # Create one hidden root window
        self.root = tk.Tk()
        self.root.withdraw()

    def start(self):
        if self.not_in_data:
            self.process_next(self.current_index)
        else:
            self.data_manager.save_dataframes()
            self.root.destroy()
        
    def process_next(self, index):
        if index < len(self.not_in_data):
            drug = self.not_in_data[index]
            # Find matches using the first word of the drug name (case-insensitive)
            first_word = drug.split()[0].lower()
            matches = self.data_manager.pdl_df[
                self.data_manager.pdl_df['pdl_name'].str.lower().str.contains(first_word, na=False)
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
            
    def open_gui_for_drug(self, drug, matches):
        def save_callback(selected_pdl_name):
            selected_row = self.data_manager.pdl_df.loc[
                self.data_manager.pdl_df['pdl_name'] == selected_pdl_name
            ].iloc[0]
            therapeutic_class = selected_row['therapeutic_class']
            status = selected_row['status']
            self.data_manager.add_status(therapeutic_class, drug, selected_pdl_name, status)
            self.data_manager.update_state_data(therapeutic_class, drug, selected_pdl_name)
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
            if self.current_index > 0:
                self.data_manager.remove_last_assignment()
                self.current_index -= 1
            self.process_next(self.current_index)
            
        selector = DrugSelectorGUI(self.root, drug, matches, save_callback, skip_callback, exit_callback, back_callback)
        selector.grab_set()  # Makes the window modal