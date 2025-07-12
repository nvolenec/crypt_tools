#!/usr/bin/python3
import tkinter as tk
from tkinter import scrolledtext
from collections import Counter, defaultdict
from math import gcd
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string

# --- Helper Functions (Decryption, Analysis, etc.) ---

def shift_letter(c, shift):
    return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))

def unshift_letter(c, shift):
    return chr((ord(c) - ord('A') - shift) % 26 + ord('A'))

def vigenere_decrypt(text, key_shifts):
    plaintext = []
    for i, c in enumerate(text):
        shift = key_shifts[i % len(key_shifts)]
        plaintext.append(unshift_letter(c, shift))
    return ''.join(plaintext)

# --- Analysis Functions ---

def match_index(text, shift, N):
    matches = sum(1 for i in range(N - shift) if text[i] == text[i + shift])
    return matches / (N - shift)

def kasiski_examination(text, n=3):
    seen = defaultdict(list)
    for i in range(len(text) - n + 1):
        seq = text[i:i + n]
        seen[seq].append(i)
    ngrams = {k: v for k, v in seen.items() if len(v) > 1}
    distances = []
    for seq, positions in ngrams.items():
        dists = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
        distances.extend(dists)
    return reduce(gcd, distances) if distances else None

def friedman_estimate(ioc, N):
    numerator = 0.0265 * N
    denominator = (ioc * (N - 1)) - (0.0385 * N) + 0.065
    return numerator / denominator

def index_of_coincidence(text):
    # Clean the text: remove non-alphabetic characters and convert to uppercase
    text = ''.join(filter(str.isalpha, text.upper()))
    N = len(text)

    if N <= 1:
        return 0.0  # Avoid division by zero

    # Count frequency of each letter
    frequencies = {letter: 0 for letter in string.ascii_uppercase}
    for letter in text:
        frequencies[letter] += 1

    # Compute the Index of Coincidence
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = N * (N - 1)

    ic = numerator / denominator if denominator != 0 else 0
    return ic
#def index_of_coincidence(text):
#    freqs = Counter(text)
#    N = len(text)
#    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))

# --- Exit Handler ---
def exit_program():
    root.quit()  # Gracefully stop the Tkinter event loop
    root.destroy()  # Destroy the window and release resources
    exit()  # Exit the program

# --- GUI Setup ---
def update_gui():
    ciphertext = ciphertext_input.get("1.0", tk.END).strip().upper()
    N = len(ciphertext)
    
    # --- Calculate Match Index vs Shift ---
    shifts = list(range(1, 31))
    match_indices = [match_index(ciphertext, s, N) for s in shifts]
    plot_match_index(shifts, match_indices)
    
    # --- Compute Index of Coincidence ---
    ioc = index_of_coincidence(ciphertext)
    ioc_label.config(text=f"Index of Coincidence (whole text): {ioc:.7f}")
    
    # --- Compute Kasiski Examination ---
    kasiski_gcd = kasiski_examination(ciphertext)
    kasiski_label.config(text=f"Kasiski GCD: {kasiski_gcd}" if kasiski_gcd else "No useful repeated trigrams")
    
    # --- Compute Friedman Estimate ---
    friedman_key_length = friedman_estimate(ioc, N)
    friedman_label.config(text=f"Friedman Estimate: {friedman_key_length:.2f}")
    
    # --- Get Manual Key Entry or Use Guessing ---
    manual_key = manual_key_entry.get().strip().upper()
    if manual_key:
        key_shifts = [ord(c) - ord('A') for c in manual_key]
        key_label.config(text=f"Manual Key: {manual_key}")
    else:
        key_length = round(friedman_key_length)  # Assuming the Friedman estimate is the key length
        columns = [ciphertext[i::key_length] for i in range(key_length)]
        
        key_shifts = []
        key_letters = []
        for col in columns:
            freqs = Counter(col)
            most_common_letter, _ = freqs.most_common(1)[0]
            shift = (ord(most_common_letter) - ord('E')) % 26
            key_shifts.append(shift)
            key_letters.append(shift_letter('A', -shift))
        
        key_label.config(text=f"Guessed Key: {''.join(key_letters)}")
    
    # Decrypt and display plaintext
    plaintext = vigenere_decrypt(ciphertext, key_shifts)
    plaintext_output.delete("1.0", tk.END)
    plaintext_output.insert(tk.END, plaintext)

def plot_match_index(shifts, match_indices):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(shifts, match_indices, marker='o')
    ax.set_title("Match Index vs Shift")
    ax.set_xlabel("Shift")
    ax.set_ylabel("Match Index")
    ax.grid(True)

    # Clear any existing plot
    for widget in graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Main Window and Layout ---
root = tk.Tk()
root.title("Vigenère Cipher Decryptor")

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

plaintext_output_label = tk.Label(central_frame, text="Plaintext:", font=("Arial", 12), fg="white", bg="black")
plaintext_output_label.pack()

plaintext_output = scrolledtext.ScrolledText(central_frame, width=50, height=10, font=("Arial", 12), bg="black", fg="white")
plaintext_output.pack()

# --- Manual Key Entry Panel ---
manual_key_label = tk.Label(central_frame, text="Enter Key (optional):", font=("Arial", 12), fg="white", bg="black")
manual_key_label.pack()

manual_key_entry = tk.Entry(central_frame, font=("Arial", 12), bg="black", fg="white")
manual_key_entry.pack()

# Analysis Panels
analysis_frame = tk.Frame(root, padx=10, pady=10, bg="black")
analysis_frame.grid(row=0, column=3, rowspan=6)

ioc_label = tk.Label(analysis_frame, text="Index of Coincidence: N/A", font=("Arial", 10), fg="white", bg="black")
ioc_label.pack()

kasiski_label = tk.Label(analysis_frame, text="Kasiski GCD: N/A", font=("Arial", 10), fg="white", bg="black")
kasiski_label.pack()

friedman_label = tk.Label(analysis_frame, text="Friedman Estimate: N/A", font=("Arial", 10), fg="white", bg="black")
friedman_label.pack()

key_label = tk.Label(analysis_frame, text="Guessed Key: N/A", font=("Arial", 12), fg="white", bg="black")
key_label.pack()

# Graph Panel
graph_frame = tk.Frame(root, padx=10, pady=10, bg="black")
graph_frame.grid(row=6, column=0, columnspan=4, pady=20)

# Action Buttons
update_button = tk.Button(root, text="Decrypt & Analyze", font=("Arial", 14), command=update_gui, bg="black", fg="white")
update_button.grid(row=7, column=0, columnspan=4, pady=10)

# Run the GUI
root.mainloop()
