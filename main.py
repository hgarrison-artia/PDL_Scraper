from app import DrugMatcherApp
from tkinter import ttk
import tkinter as tk
from data_manager import DataManager
import sys

def clear_old_pairings(state, process_type):
    """Clear old drug pairings for the selected state"""
    data_manager = DataManager(state, process_type)
    data_manager.clear_old_drug_pairings()

def select_pharmacy_or_clinical():
    """Create a dialog to select between Pharmacy and Clinical processing"""
    root = tk.Tk()
    root.title("Select Processing Type")
    
    # Set window size and background color
    root.geometry("400x300")
    root.configure(bg="#00314C")
    
    # Force the window to appear on top and grab focus
    root.attributes('-topmost', True)
    root.update()
    root.after(100, lambda: root.attributes('-topmost', False))
    
    # Create and configure styles
    style = ttk.Style(root)
    style.theme_use("clam")
    
    # Configure styles for dark theme
    style.configure("TFrame",
        background="#00314C"
    )
    
    style.configure("TLabel", 
        font=("Helvetica", 16),
        background="#00314C",
        foreground="white",
        padding=10
    )
    
    style.configure("TRadiobutton",
        font=("Helvetica", 14),
        background="#00314C",
        foreground="white",
        padding=5
    )
    
    style.map("TRadiobutton",
        background=[('active', '#00314C')],
        foreground=[('active', 'white')]
    )
    
    style.configure("TButton",
        font=("Helvetica", 14),
        padding=10,
        background="#00314C",
        foreground="white"
    )
    
    style.map("TButton",
        background=[('active', '#004B6B')],
        foreground=[('active', 'white')]
    )
    
    # Create main frame
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Title label
    title_label = ttk.Label(main_frame, text="Select Processing Type:", style="TLabel")
    title_label.pack(pady=(0, 20))
    
    # Create a variable to hold the selection
    selection_var = tk.StringVar(value="Pharmacy")
    
    # Create radio buttons
    pharmacy_radio = ttk.Radiobutton(
        main_frame,
        text="Pharmacy",
        variable=selection_var,
        value="Pharmacy",
        style="TRadiobutton"
    )
    pharmacy_radio.pack(anchor=tk.W, padx=40, pady=5)
    
    clinical_radio = ttk.Radiobutton(
        main_frame,
        text="Clinical",
        variable=selection_var,
        value="Clinical",
        style="TRadiobutton"
    )
    clinical_radio.pack(anchor=tk.W, padx=40, pady=5)
    
    # Function to handle selection and close window
    def submit():
        root.quit()
        root.destroy()
    
    # Submit button
    submit_button = ttk.Button(
        main_frame,
        text="Submit",
        command=submit,
        style="TButton"
    )
    submit_button.pack(pady=20)
    
    # Exit button
    def exit_app():
        root.quit()
        root.destroy()
        sys.exit(0)
    
    exit_button = ttk.Button(
        main_frame,
        text="Exit",
        command=exit_app,
        style="TButton"
    )
    exit_button.pack(pady=10)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run the selection loop
    root.mainloop()
    return selection_var.get()

def clear_all_states_pairings(process_type):
    """Clear old drug pairings for all states"""
    states = ["AK", "AL", "CT", "FL", "GA", "IA", "IL", "LA", "ME", "MS", "NC", "NH", "OH", "OR", "TN", "UT", "WA"]
    for state in states:
        data_manager = DataManager(state, process_type)
        data_manager.clear_old_drug_pairings()

def select_state():
    # Create a temporary window for state selection
    root = tk.Tk()
    root.title("Select State")
    
    # Set window size and background color
    root.geometry("600x900")  # Increased height from 800 to 900
    root.configure(bg="#00314C")
    
    # Force the window to appear on top and grab focus
    root.attributes('-topmost', True)
    root.update()
    # Turn off topmost after a short delay so it doesn't interfere later
    root.after(100, lambda: root.attributes('-topmost', False))
    
    # Create and configure styles
    style = ttk.Style(root)
    style.theme_use("clam")
    
    # Configure styles for dark theme
    style.configure("TFrame",
        background="#00314C"
    )
    
    style.configure("TLabel", 
        font=("Helvetica", 16),
        background="#00314C",
        foreground="white",
        padding=10
    )
    
    style.configure("TRadiobutton",
        font=("Helvetica", 14),
        background="#00314C",
        foreground="white",
        padding=5
    )
    
    style.map("TRadiobutton",
        background=[('active', '#00314C')],
        foreground=[('active', 'white')]
    )
    
    style.configure("TButton",
        font=("Helvetica", 14),
        padding=10,
        background="#00314C",
        foreground="white"
    )
    
    style.map("TButton",
        background=[('active', '#004B6B')],
        foreground=[('active', 'white')]
    )
    
    # Create main frame
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Configure grid columns to expand equally for centering
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    
    # Title label
    title_label = ttk.Label(main_frame, text="Select a State:", style="TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
    
    # Create a variable to hold the selection; default is "LA"
    state_var = tk.StringVar(value="AK")
    
    # List of available states
    states = ["AK", "AL", "CT", "FL", "GA", "IA", "IL", "LA", "ME", "MS", "NC", "NH", "OH", "OR", "TN", "UT", "WA"]
    
    # Create radio buttons for each state in two columns
    num_columns = 2
    for idx, st in enumerate(states):
        row = 1 + idx // num_columns
        col = idx % num_columns
        radio = ttk.Radiobutton(
            main_frame,
            text=st,
            variable=state_var,
            value=st,
            style="TRadiobutton"
        )
        radio.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
    
    # Function to clear old pairings and destroy the window when submit is clicked
    def submit():
        selected_state = state_var.get()
        root.quit()
        root.destroy()
        
        # Get process type
        process_type = select_pharmacy_or_clinical()
        if process_type is not None:
            # Clear old pairings
            clear_old_pairings(selected_state, process_type)
            # Initialize the main application with the selected state and process type
            app = DrugMatcherApp(selected_state, process_type)
            app.start()
            # Start the Tkinter event loop
            app.root.mainloop()
    
    # Submit button
    submit_button = ttk.Button(
        main_frame,
        text="Submit",
        command=submit,
        style="TButton"
    )
    submit_button.grid(row=len(states)//num_columns+2, column=0, columnspan=2, pady=20, sticky="ew")
    
    # Clear old pairings button
    def clear_pairings():
        selected_state = state_var.get()
        process_type = select_pharmacy_or_clinical()
        if process_type is not None:
            clear_old_pairings(selected_state, process_type)
    
    clear_button = ttk.Button(
        main_frame,
        text="Clear Old Drug Pairings",
        command=clear_pairings,
        style="TButton"
    )
    clear_button.grid(row=len(states)//num_columns+3, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Clear all states pairings button
    def clear_all_states():
        process_type = select_pharmacy_or_clinical()
        if process_type is not None:
            clear_all_states_pairings(process_type)
    
    clear_all_button = ttk.Button(
        main_frame,
        text="Clear All States Drug Pairings",
        command=clear_all_states,
        style="TButton"
    )
    clear_all_button.grid(row=len(states)//num_columns+4, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Exit button
    def exit_app():
        root.quit()
        root.destroy()
        sys.exit(0)  # This will completely terminate the Python process
    
    exit_button = ttk.Button(
        main_frame,
        text="Exit",
        command=exit_app,
        style="TButton"
    )
    exit_button.grid(row=len(states)//num_columns+5, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run the state selection loop and return the chosen state
    root.mainloop()
    return state_var.get()

def main():
    # Prompt the user to select a state using the GUI
    state = select_state()
    
    # Only proceed if state is not None (which happens when Exit is clicked)
    if state is not None:
        # The rest of the processing is now handled in the submit function
        pass

if __name__ == '__main__':
    main()