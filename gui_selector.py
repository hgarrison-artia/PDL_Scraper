import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk
from PIL import Image, ImageTk

class DrugSelectorGUI(Toplevel):
    # Theme colors - only dark mode
    theme = {
        'bg': "#00314C",  # Dark blue background
        'fg': "white",    # White text
        'select_bg': "#0078d7",
        'select_fg': "white",
        'button_bg': "#00314C",  # Match background for buttons
        'button_fg': "white",    # White text for buttons
        'button_active_bg': "#004B6B",  # Slightly lighter blue for button hover
        'button_active_fg': "white"     # White text for button hover
    }

    def __init__(self, master, drug, matches, save_callback, skip_callback, exit_callback, back_callback, current_index, total_drugs, save_to_all_callback=None):
        super().__init__(master)
        self.title(f"Select Match for {drug}")
        
        self.configure(bg=self.theme['bg'])

        self.drug = drug
        self.matches = matches
        self.save_callback = save_callback
        self.skip_callback = skip_callback
        self.exit_callback = exit_callback
        self.back_callback = back_callback
        self.save_to_all_callback = save_to_all_callback
        self.current_index = current_index
        self.total_drugs = total_drugs

        self.center_window(1200, 800)
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
        style.theme_use("clam")
        
        # Configure button style
        style.configure("TButton", 
            font=("Helvetica", 12), 
            padding=8,
            background=self.theme['button_bg'],
            foreground=self.theme['button_fg']
        )
        style.map("TButton",
            background=[('active', self.theme['button_active_bg'])],
            foreground=[('active', self.theme['button_active_fg'])]
        )
        
        # Configure label style
        style.configure("TLabel", 
            font=("Helvetica", 14), 
            padding=8,
            background=self.theme['bg'],
            foreground=self.theme['fg']
        )
        
        # Configure frame style
        style.configure("TFrame", 
            background=self.theme['bg']
        )

        # Create header frame for logo and title
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Load and display the logo
        try:
            logo_image = Image.open("Artia_Logo.png")
            # Resize logo to appropriate height while maintaining aspect ratio
            logo_height = 50
            aspect_ratio = logo_image.width / logo_image.height
            logo_width = int(logo_height * aspect_ratio)
            logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = ttk.Label(header_frame, image=self.logo_photo, style="TLabel")
            logo_label.grid(row=0, column=0, padx=(0, 20))
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Create and place the label next to the logo
        label = ttk.Label(header_frame, text=f"Select a match for: {self.drug}", style="TLabel")
        label.grid(row=0, column=1, padx=10, pady=10)

        # Add progress label
        remaining = self.total_drugs - self.current_index
        progress_label = ttk.Label(self, text=f"Remaining drugs to process: {remaining}", style="TLabel")
        progress_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Use a Tkinter Listbox for the match list with larger font and increased size
        self.listbox = tk.Listbox(
            self, 
            width=100,
            height=20,
            font=("Helvetica", 14),
            bg=self.theme['bg'],
            fg=self.theme['fg'],
            selectbackground=self.theme['select_bg'],
            selectforeground=self.theme['select_fg'],
            highlightthickness=0,  # Remove border
            relief="flat"  # Remove border
        )
        self.listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        # Populate the listbox with the match options
        for _, row in self.matches.iterrows():
            self.listbox.insert(tk.END, f"{row['pdl_name']} | {row['therapeutic_class']} | {row['status']}")

        # Create a frame for buttons to better organize them
        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Add the Back button
        btn_back = ttk.Button(button_frame, text="Back", command=self.back, style="TButton")
        btn_back.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Create another frame for action buttons
        action_frame = ttk.Frame(self, style="TFrame")
        action_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Save, Save to All, Skip, and Exit buttons
        btn_save = ttk.Button(action_frame, text="Save", command=self.save_selection, style="TButton")
        btn_save.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        btn_save_all = ttk.Button(action_frame, text="Save to All", command=self.save_to_all, style="TButton")
        btn_save_all.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_skip = ttk.Button(action_frame, text="Skip", command=self.skip_drug, style="TButton")
        btn_skip.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        btn_exit = ttk.Button(action_frame, text="Exit and Save", command=self.exit_program, style="TButton")
        btn_exit.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Configure grid weights for better spacing
        self.grid_rowconfigure(2, weight=1)  # Make the listbox row expandable
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        # Configure header frame columns
        header_frame.columnconfigure(1, weight=1)
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Configure action frame columns
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)
        action_frame.columnconfigure(3, weight=1)

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

    def save_to_all(self):
        selected_index = self.listbox.curselection()
        if selected_index and self.save_to_all_callback:
            selected_text = self.listbox.get(selected_index[0])
            selected_drug = selected_text.split(" | ")[0]  # Extract pdl_name
            self.save_to_all_callback(selected_drug)
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