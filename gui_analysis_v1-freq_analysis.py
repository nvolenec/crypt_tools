import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import re
from collections import Counter

# --- Helper Functions ---
def clean_ciphertext(text, regex_pattern, respect_spaces):
    # Remove unwanted characters based on the regex and user's choice of respecting spaces/punctuation
    if respect_spaces:
        # Only remove non-alphabetic characters excluding spaces
        cleaned_text = re.sub(r'[^A-Za-z ]+', '', text)
    else:
        # Remove all non-alphabetic characters (including spaces)
        cleaned_text = re.sub(regex_pattern, '', text)
    return cleaned_text

def index_of_coincidence(text):
    text = [ch for ch in text if ch.isalpha()]  # Ignore spaces and non-alphabet characters
    N = len(text)
    if N < 2:  # Avoid division by zero
        return 0
    freqs = Counter(text)
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))

def frequency_analysis(text):
    text = [ch for ch in text if ch.isalpha()]  # Ignore spaces and non-alphabet characters
    freqs = Counter(text)
    total = len(text)
    analysis = {letter: count / total for letter, count in freqs.items()}
    return analysis

# --- GUI Setup ---

def update_gui():
    # Get the user input for ciphertext and settings
    ciphertext = ciphertext_input.get("1.0", tk.END).strip()
    regex_pattern = regex_input.get().strip()
    respect_spaces = respect_spaces_var.get()

    if not ciphertext:
        messagebox.showwarning("Input Error", "Please provide some ciphertext for analysis.")
        return

    # Clean the ciphertext according to user preferences
    cleaned_text = clean_ciphertext(ciphertext, regex_pattern, respect_spaces)

    # --- Frequency Analysis ---
    freq_analysis = frequency_analysis(cleaned_text)

    # Clear previous results
    freq_output.delete(1.0, tk.END)
    freq_output.insert(tk.END, "Letter Frequency Analysis:\n\n")
    for letter, freq in sorted(freq_analysis.items()):
        freq_output.insert(tk.END, f"{letter}: {freq:.4f}\n")

    # --- Index of Coincidence ---
    ioc = index_of_coincidence(cleaned_text)
    ioc_label.config(text=f"Index of Coincidence: {ioc:.7f}")

def exit_program():
    root.quit()  # Gracefully stop the Tkinter event loop
    root.destroy()  # Destroy the window and release resources
    exit()  # Exit the program

# --- Main Window and Layout ---
root = tk.Tk()
root.title("Ciphertext Analysis")

# Set the background color of the root window to black
root.config(bg="black")

# Attach the exit handler to the window close event
root.protocol("WM_DELETE_WINDOW", exit_program)

# Central Frame (Ciphertext, Plaintext)
central_frame = tk.Frame(root, padx=10, pady=10, bg="black")
central_frame.grid(row=0, column=0, rowspan=6, columnspan=3)

ciphertext_input_label = tk.Label(central_frame, text="Ciphertext:", font=("Arial", 12), fg="white", bg="black")
ciphertext_input_label.pack()

ciphertext_input = scrolledtext.ScrolledText(central_frame, width=50, height=10, font=("Arial", 12), bg="black", fg="white")
ciphertext_input.pack()

regex_label = tk.Label(central_frame, text="Letter Separator Regex (e.g., '\\W'):", font=("Arial", 12), fg="white", bg="black")
regex_label.pack()

regex_input = tk.Entry(central_frame, font=("Arial", 12), bg="black", fg="white")
regex_input.pack()

# Respect Spaces Checkbox
respect_spaces_var = tk.BooleanVar(value=True)
respect_spaces_checkbox = tk.Checkbutton(central_frame, text="Respect Spaces and Punctuation", font=("Arial", 12), fg="white", bg="black", variable=respect_spaces_var)
respect_spaces_checkbox.pack()

# Analysis Panels
analysis_frame = tk.Frame(root, padx=10, pady=10, bg="black")
analysis_frame.grid(row=0, column=3, rowspan=6)

ioc_label = tk.Label(analysis_frame, text="Index of Coincidence: N/A", font=("Arial", 10), fg="white", bg="black")
ioc_label.pack()

freq_output_label = tk.Label(analysis_frame, text="Frequency Analysis:", font=("Arial", 12), fg="white", bg="black")
freq_output_label.pack()

freq_output = scrolledtext.ScrolledText(analysis_frame, width=30, height=10, font=("Arial", 10), bg="black", fg="white")
freq_output.pack()

# Action Button
update_button = tk.Button(root, text="Analyze Ciphertext", font=("Arial", 14), command=update_gui, bg="black", fg="white")
update_button.grid(row=7, column=0, columnspan=4, pady=10)

# Run the GUI
root.mainloop()
