import tkinter as tk
from tkinter import ttk, scrolledtext
from collections import Counter
import string
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def frequency_analysis(text):
    t = [ch for ch in text if ch.isalnum()]
    return Counter(t)


def process_input():
    raw_text = input_text.get("1.0", tk.END).strip()
    separator = separator_entry.get()
    print( raw_text )
    print( "'"+separator+"'" )
    
    if separator:
        #cleaned_text = "".join(raw_text.split(separator))
        #cleaned_text = join(raw_text.split(separator))
        cleaned_text = raw_text
    else:
        cleaned_text = raw_text.replace(" ", "")
    print( cleaned_text )

    #cleaned_text = ''.join(filter(str.isalpha, cleaned_text.upper()))
    cleaned_text = ''.join(cleaned_text.upper())

    # Compute Index of Coincidence
    ic = index_of_coincidence(cleaned_text)

    cleaned_text2 = re.split( separator, cleaned_text )
    # Frequency analysis
    freq = frequency_analysis(cleaned_text2)
    sorted_freq = sorted(freq.items())

    # Display results
    ic_result.config(text=f"Index of Coincidence: {ic}")
    freq_result.delete("1.0", tk.END)
    for letter, count in sorted_freq:
        freq_result.insert(tk.END, f"{letter}: {count}\n")

    # Plot frequencies
    plot_frequency(sorted_freq)


def plot_frequency(freq_data):
    letters = [item[0] for item in freq_data]
    counts = [item[1] for item in freq_data]

    fig.clear()
    ax = fig.add_subplot(111)
    bars = ax.bar(letters, counts, color='red')
    for bar in bars:
        height = bar.get_height()
        ax.text( 
                bar.get_x() + bar.get_width() /2,
                height + 0.5,
                str(height),
                ha='center',
                va='bottom',
                color='white',
                fontsize=8
                )
    ax.set_title("Letter Frequency")
    ax.set_xlabel("Letter")
    ax.set_ylabel("Count")
    ax.set_facecolor("black")
    ax.tick_params(colors='white')
    fig.tight_layout()

    canvas.draw()


# GUI Setup
root = tk.Tk()
root.title("Ciphertext Analyzer")
root.configure(bg='black')

# Ciphertext input
tk.Label(root, text="Enter Ciphertext:", fg='white', bg='black').pack(anchor='w')
input_text = scrolledtext.ScrolledText(root, height=6, insertbackground='red', wrap=tk.WORD)
input_text.pack(fill='x', padx=5, pady=5)

# Separator input
tk.Label(root, text="Letter Separator:", fg='white', bg='black').pack(anchor='w')
separator_entry = tk.Entry(root, insertbackground='red')
separator_entry.pack(fill='x', padx=5, pady=5)

# Process Button
process_btn = tk.Button(root, text="Analyze", command=process_input)
process_btn.pack(pady=10)

# IC Result
ic_result = tk.Label(root, text="", fg='white', bg='black', font=('Courier', 12))
ic_result.pack()

# Frequency Result
tk.Label(root, text="Frequency Analysis:", fg='white', bg='black').pack(anchor='w')
freq_result = scrolledtext.ScrolledText(root, height=8, insertbackground='red', wrap=tk.WORD)
freq_result.pack(fill='x', padx=5, pady=5)

# Frequency Plot
fig = plt.Figure(figsize=(6, 3), facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True)

root.mainloop()
