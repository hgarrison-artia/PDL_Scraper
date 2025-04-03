import tkinter as tk
from tkinter import ttk
from app import DrugMatcherApp

def select_state():
    # Create a temporary window for state selection
    root = tk.Tk()
    root.title("Select State")
    
    # Force the window to appear on top and grab focus
    root.attributes('-topmost', True)
    root.update()
    # Turn off topmost after a short delay so it doesn't interfere later
    root.after(100, lambda: root.attributes('-topmost', False))
    
    ttk.Label(root, text="Select a state:", font=("Helvetica", 12)).pack(padx=10, pady=10)
    
    # Create a variable to hold the selection; default is "LA"
    state_var = tk.StringVar(value="LA")
    
    # List of available states
    states = ["AK", "CO", "FL", "GA", "IA", "IL", "LA", "MS", "TN"]
    
    # Create radio buttons for each state
    for st in states:
        ttk.Radiobutton(root, text=st, variable=state_var, value=st).pack(anchor=tk.W, padx=20, pady=2)
    
    # Function to destroy the window when submit is clicked
    def submit():
        root.destroy()
    
    ttk.Button(root, text="Submit", command=submit).pack(pady=10)
    
    # Run the state selection loop and return the chosen state
    root.mainloop()
    return state_var.get()

def main():
    # Prompt the user to select a state using the GUI
    state = select_state()
    
    # Initialize the main application with the selected state
    app = DrugMatcherApp(state)
    app.start()
    
    # Start the main event loop (the hidden root window is used for the rest of the application)
    app.root.mainloop()

if __name__ == '__main__':
    main()