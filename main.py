from app import DrugMatcherApp
from tkinter import ttk
import tkinter as tk

def select_state():
    # Create a temporary window for state selection
    root = tk.Tk()
    root.title("Select State")
    
    # Set window size and background color
    root.geometry("600x800")
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
    
    # Title label
    title_label = ttk.Label(main_frame, text="Select a State:", style="TLabel")
    title_label.pack(pady=(0, 20))
    
    # Create a variable to hold the selection; default is "LA"
    state_var = tk.StringVar(value="AK")
    
    # List of available states
    states = ["AK", "AL", "CT", "CO", "FL", "GA", "IA", "IL", "LA", "MS", "TN"]
    
    # Create radio buttons for each state
    for st in states:
        radio = ttk.Radiobutton(
            main_frame,
            text=st,
            variable=state_var,
            value=st,
            style="TRadiobutton"
        )
        radio.pack(anchor=tk.W, padx=40, pady=5)
    
    # Function to destroy the window when submit is clicked
    def submit():
        root.destroy()
    
    # Submit button
    submit_button = ttk.Button(
        main_frame,
        text="Submit",
        command=submit,
        style="TButton"
    )
    submit_button.pack(pady=20)
    
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

    # Initialize the main application with the selected state
    app = DrugMatcherApp(state)
    app.start()
    # Start the Tkinter event loop
    app.root.mainloop()

if __name__ == '__main__':
    main()