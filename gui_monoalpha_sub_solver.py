import tkinter as tk
from tkinter import ttk
from collections import Counter
import string
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SubstitutionCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mono-Alphabetic Substitution Cipher Breaker")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # State
        self.ciphertext = ""
        self.mapping = {letter: letter for letter in string.ascii_uppercase}

        # GUI Layout
        self.create_widgets()

    def create_widgets(self):
        # Top: Ciphertext input
        tk.Label(self.root, text="Ciphertext:").pack(anchor="w")
        self.cipher_input = tk.Text(self.root, height=5, width=100)
        self.cipher_input.pack()
        self.cipher_input.bind("<KeyRelease>", self.on_ciphertext_change)

        # Middle: Mapping inputs
        self.mapping_frame = tk.Frame(self.root)
        self.mapping_frame.pack(pady=5)

        self.mapping_vars = {}
        for idx, letter in enumerate(string.ascii_uppercase):
            tk.Label(self.mapping_frame, text=letter).grid(row=0, column=idx)
            var = tk.StringVar(value=letter)
            entry = tk.Entry(self.mapping_frame, textvariable=var, width=2, justify='center')
            entry.grid(row=1, column=idx)
            var.trace_add("write", self.on_mapping_change)
            self.mapping_vars[letter] = var

        # Bottom: Plaintext output
        tk.Label(self.root, text="Plaintext:").pack(anchor="w")
        self.plain_output = tk.Text(self.root, height=5, width=100, state=tk.DISABLED)
        self.plain_output.pack()

        # Graph: Frequency analysis
        self.figure, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

    def on_ciphertext_change(self, event=None):
        self.ciphertext = self.cipher_input.get("1.0", tk.END).upper()
        self.ciphertext = ''.join(filter(str.isalpha, self.ciphertext))  # Clean non-alpha
        self.reset_mapping()
        self.update_plaintext()
        self.update_graph()

    def reset_mapping(self):
        used = set()
        for letter in string.ascii_uppercase:
            default = letter
            while default in used:
                default = chr((ord(default) - 65 + 1) % 26 + 65)
            used.add(default)
            self.mapping_vars[letter].set(default)

    def on_mapping_change(self, *args):
        # Build reverse map to remove duplicates
        reverse_map = {}
        for cipher_letter, var in self.mapping_vars.items():
            val = var.get().upper()
            if val in string.ascii_uppercase and val not in reverse_map.values():
                reverse_map[cipher_letter] = val
            else:
                reverse_map[cipher_letter] = ''  # Empty if invalid or duplicate

        # Update mapping dict and fix conflicts
        for k, v in reverse_map.items():
            self.mapping[k] = v if v in string.ascii_uppercase else '?'

        self.update_plaintext()
        self.update_graph()

    def update_plaintext(self):
        translated = ""
        for char in self.ciphertext:
            translated += self.mapping.get(char, '?')

        self.plain_output.config(state=tk.NORMAL)
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.insert(tk.END, translated)
        self.plain_output.config(state=tk.DISABLED)

    def update_graph(self):
        self.ax.clear()
        counts = Counter(self.ciphertext)
        letters = list(string.ascii_uppercase)
        freqs = [counts.get(letter, 0) for letter in letters]

        self.ax.bar(letters, freqs, color='skyblue')
        self.ax.set_title("Letter Frequency in Ciphertext")
        self.ax.set_ylabel("Frequency")
        self.ax.set_xlabel("Letter")
        self.figure.tight_layout()
        self.canvas.draw()

    def on_close(self):
        print("Closing application gracefully...")
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SubstitutionCipherApp(root)
    root.mainloop()

