import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk

class DrugSelectorGUI(Toplevel):
    def __init__(self, master, drug, matches, save_callback, skip_callback, exit_callback):
        super().__init__(master)
        self.title(f"Select Match for {drug}")
        self.geometry("600x400+100+100")
        self.configure(bg="#f0f0f0")  # Light gray background

        self.drug = drug
        self.matches = matches
        self.save_callback = save_callback
        self.skip_callback = skip_callback
        self.exit_callback = exit_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        # Use ttk styles to create a more modern look
        style = ttk.Style(self)
        style.theme_use("clam")  # You can experiment with other available themes
        style.configure("TButton", font=("Helvetica", 10), padding=6)
        style.configure("TLabel", font=("Helvetica", 12), padding=6)
        
        # Create and place the label
        label = ttk.Label(self, text=f"Select a match for: {self.drug}", background="#f0f0f0")
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        # Use a Tkinter Listbox for the match list with custom font
        self.listbox = tk.Listbox(self, width=80, height=10, font=("Helvetica", 10))
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Populate the listbox with the match options
        for _, row in self.matches.iterrows():
            self.listbox.insert(tk.END, f"{row['pdl_name']} | {row['therapeutic_class']} | {row['status']}")
        
        # Save button
        btn_save = ttk.Button(self, text="Save", command=self.save_selection)
        btn_save.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Skip button
        btn_skip = ttk.Button(self, text="Skip", command=self.skip_drug)
        btn_skip.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Exit button
        btn_exit = ttk.Button(self, text="Exit and Save", command=self.exit_program)
        btn_exit.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        
        # Ensure the columns expand evenly
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
    def save_selection(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index[0])
            selected_drug = selected_text.split(" | ")[0]  # Extract pdl_name
            self.save_callback(selected_drug)
        self.destroy()
        
    def skip_drug(self):
        self.skip_callback()
        self.destroy()
        
    def exit_program(self):
        self.exit_callback()
