import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv

# ---------------------------------------------------
# 1. Read the CSV Files and Prepare Status Options
# ---------------------------------------------------

# Read statuses.csv.
# Expecting two columns: "Non-Preferred" and "Preferred" (each with a list of drug names)
statuses_df = pd.read_csv("statuses.csv")
non_preferred_list = statuses_df["Non-Preferred"].dropna().tolist()
preferred_list = statuses_df["Preferred"].dropna().tolist()

# Build a list of tuples: (status_drug_name, PDL_status)
status_options = []
for drug_name in non_preferred_list:
    status_options.append((drug_name, "Non-Preferred"))
for drug_name in preferred_list:
    status_options.append((drug_name, "Preferred"))

# Read drugs.csv which now has at least two columns: "Drugs" and "Class"
drugs_df = pd.read_csv("drugs.csv")
# Get the unique classes (sorted alphabetically) from the drugs data.
classes = sorted(drugs_df["Class"].dropna().unique())

# ---------------------------------------------------
# 2. Global Variables for the Process
# ---------------------------------------------------
current_index = 0           # index of the current drug from the filtered list
saved_records = []          # to hold records where the user made a selection (for output.csv)
non_pdl_records = []        # to hold drugs auto-assigned "Non PDL" (for non_pdl.csv)
skipped_records = []        # to hold drugs skipped by the user (for skipped.csv)
current_viable_options = [] # candidate statuses for the current drug
drugs = []                  # will be set to the list of drugs from the selected classes

# ---------------------------------------------------
# 3. Functions for Drug Processing
# ---------------------------------------------------

def process_next_drug():
    """
    Process the next drug in the filtered drugs list.
    If the first word of the drug is found in one or more status entries,
    update the GUI accordingly. If not, record it as "Non PDL" in a separate list,
    then move on.
    """
    global current_index, current_viable_options, drugs
    if current_index >= len(drugs):
        write_output_files()
        root.destroy()
        return

    current_drug = drugs[current_index]
    # Extract the first word (assuming words are split by whitespace)
    first_word = current_drug.split()[0]

    # Look for statuses where the first word is a substring (case-insensitive)
    viable_options = []
    for status_drug, pdl_status in status_options:
        if first_word.lower() in status_drug.lower():
            viable_options.append((status_drug, pdl_status))
            
    # Sort the viable options alphabetically by the status drug name (ignoring case)
    viable_options = sorted(viable_options, key=lambda x: x[0].lower())

    if len(viable_options) == 0:
        # Record as "Non PDL" in the separate list
        non_pdl_records.append((current_drug, "Non PDL", "Non PDL"))
        current_index += 1
        process_next_drug()
    else:
        # Update the GUI with the current drug and the viable status options.
        label_drug.config(text="Drug to check: " + current_drug)
        listbox_options.delete(0, tk.END)
        for option in viable_options:
            listbox_options.insert(tk.END, f"{option[0]} ({option[1]})")
        current_viable_options = viable_options
        listbox_options.selection_clear(0, tk.END)

def save_selection():
    """
    Save the currently selected candidate from the listbox.
    The saved record is added to saved_records (for output.csv).
    """
    global current_index
    selected_indices = listbox_options.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No selection made. Please select an option or click Skip.")
        return

    selected_idx = selected_indices[0]
    chosen_option = current_viable_options[selected_idx]
    current_drug = drugs[current_index]
    saved_records.append((current_drug, chosen_option[0], chosen_option[1]))
    current_index += 1
    process_next_drug()

def skip_drug():
    """
    Skip saving the current drug.
    The skipped drug is recorded in skipped_records (for skipped.csv).
    """
    global current_index
    skipped_records.append(drugs[current_index])
    current_index += 1
    process_next_drug()

def write_output_files():
    """
    Write the saved records (manual selections) to output.csv,
    the auto-assigned "Non PDL" drugs to non_pdl.csv, and the
    skipped drugs to skipped.csv.
    """
    # Write manual selections to output.csv
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Drug", "Matched Drug", "PDL Status"])
        for record in saved_records:
            writer.writerow(record)
    # Write auto-assigned "Non PDL" drugs to non_pdl.csv
    with open("non_pdl.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Drug", "Matched Drug", "PDL Status"])
        for record in non_pdl_records:
            writer.writerow(record)
    # Write skipped drugs to skipped.csv
    with open("skipped.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Drug"])
        for drug in skipped_records:
            writer.writerow([drug])
    print("Output saved to output.csv, non_pdl.csv, and skipped.csv")

# ---------------------------------------------------
# 4. Build the Main GUI Window for Drug Processing
# ---------------------------------------------------
root = tk.Tk()
root.title("Drug Status Checker")

# Label to show the current drug
label_drug = tk.Label(root, text="Drug to check:")
label_drug.pack(pady=10)

# Listbox to display viable status options (single-select)
listbox_options = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
listbox_options.pack(padx=10, pady=5)

# Frame to hold the Save and Skip buttons side-by-side
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)
button_save = tk.Button(frame_buttons, text="Save", width=10, command=save_selection)
button_save.pack(side=tk.LEFT, padx=5)
button_skip = tk.Button(frame_buttons, text="Skip", width=10, command=skip_drug)
button_skip.pack(side=tk.LEFT, padx=5)

# ---------------------------------------------------
# 5. Create the Class Selection Window with a Scrollable Canvas
# ---------------------------------------------------
class_selection_window = tk.Toplevel(root)
class_selection_window.title("Select Drug Classes")
# Optional: set a fixed geometry for the class selection window
# class_selection_window.geometry("320x400")

# Label at the top of the class selection window
label_select = tk.Label(class_selection_window, text="Select Classes to Process:")
label_select.pack(pady=5)

# Create a canvas and attach a vertical scrollbar
canvas = tk.Canvas(class_selection_window, borderwidth=0, width=300, height=300)
scrollbar = tk.Scrollbar(class_selection_window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas that will contain the checkbuttons
checkbutton_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=checkbutton_frame, anchor="nw")

def onFrameConfigure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

checkbutton_frame.bind("<Configure>", onFrameConfigure)

# Dictionary to hold a BooleanVar for each class
class_vars = {}

# "Select All" option at the top of the checkbutton frame
select_all_var = tk.BooleanVar(value=False)
def toggle_select_all():
    state = select_all_var.get()
    for var in class_vars.values():
        var.set(state)
select_all_cb = tk.Checkbutton(checkbutton_frame, text="Select All", variable=select_all_var, command=toggle_select_all)
select_all_cb.pack(anchor="w")

# Create a checkbutton for each class
for cls in classes:
    var = tk.BooleanVar(value=False)
    class_vars[cls] = var
    cb = tk.Checkbutton(checkbutton_frame, text=cls, variable=var)
    cb.pack(anchor="w")

def start_processing():
    """
    Called when the user clicks the Start button.
    Filters the drugs based on the selected classes and begins processing.
    """
    global drugs, current_index
    selected = [cls for cls, var in class_vars.items() if var.get()]
    if not selected:
        messagebox.showerror("Error", "Please select at least one class.")
        return
    filtered_df = drugs_df[drugs_df["Class"].isin(selected)]
    if filtered_df.empty:
        messagebox.showerror("Error", "No drugs found for the selected classes.")
        return
    # Update the global drugs list with only those from the selected classes.
    drugs = filtered_df["Drugs"].dropna().tolist()
    current_index = 0
    # Close the class selection window and start processing.
    class_selection_window.destroy()
    process_next_drug()

# Add a Start button at the bottom of the class selection window.
tk.Button(class_selection_window, text="Start", command=start_processing).pack(pady=10)

# ---------------------------------------------------
# 6. Start the GUI Event Loop
# ---------------------------------------------------
root.mainloop()
