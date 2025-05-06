import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk

class DrugSelectorGUI(Toplevel):
    def __init__(self, master, drug, matches, save_callback, skip_callback, exit_callback, back_callback):
        super().__init__(master)
        self.title(f"Select Match for {drug}")
        self.configure(bg="#f0f0f0")  # Light gray background

        self.drug = drug
        self.matches = matches
        self.save_callback = save_callback
        self.skip_callback = skip_callback
        self.exit_callback = exit_callback
        self.back_callback = back_callback

        self.center_window(900, 600)  # Set window size to 900x600 and center it
        self.create_widgets()

    def center_window(self, width, height):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Calculate x and y coordinates for the window to be centered
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Use ttk styles to create a more modern look
        style = ttk.Style(self)
        style.theme_use("clam")  # You can experiment with other available themes
        style.configure("TButton", font=("Helvetica", 12), padding=8)
        style.configure("TLabel", font=("Helvetica", 14), padding=8)

        # Create and place the label
        label = ttk.Label(self, text=f"Select a match for: {self.drug}", background="#f0f0f0")
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Use a Tkinter Listbox for the match list with larger font and increased size
        self.listbox = tk.Listbox(self, width=80, height=15, font=("Helvetica", 14))
        self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        # Populate the listbox with the match options
        for _, row in self.matches.iterrows():
            self.listbox.insert(tk.END, f"{row['pdl_name']} | {row['therapeutic_class']} | {row['status']}")

        # Add the Back button on row 2 spanning all columns
        btn_back = ttk.Button(self, text="Back", command=self.back)
        btn_back.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Save, Skip, and Exit buttons on row 3
        btn_save = ttk.Button(self, text="Save", command=self.save_selection)
        btn_save.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        btn_skip = ttk.Button(self, text="Skip", command=self.skip_drug)
        btn_skip.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        btn_exit = ttk.Button(self, text="Exit and Save", command=self.exit_program)
        btn_exit.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        # Ensure the columns expand evenly
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def on_double_click(self, event):
        """Handler for double-click events in the listbox to trigger save functionality."""
        self.save_selection()

    def save_selection(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index[0])
            selected_drug = selected_text.split(" | ")[0]  # Extract pdl_name
            self.save_callback(selected_drug)
        try:
            self.destroy()
        except tk.TclError:
            None

    def skip_drug(self):
        self.skip_callback()
        try:
            self.destroy()
        except tk.TclError:
            None

    def exit_program(self):
        self.exit_callback()
        try:
            self.destroy()
        except tk.TclError:
            None

    def back(self):
        self.back_callback()
        try:
            self.destroy()
        except tk.TclError:
            None