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

        self.ciphertext = ""
        self.mapping = {letter: letter for letter in string.ascii_uppercase}

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Ciphertext input
        tk.Label(self.root, text="Ciphertext:").pack(anchor="w")
        self.cipher_input = tk.Text(self.root, height=10, width=100)
        self.cipher_input.pack()
        self.cipher_input.bind("<KeyRelease>", self.on_ciphertext_change)

        # Mapping inputs
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

        # Analyze button
        self.analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_plaintext)
        self.analyze_button.pack(pady=5)

        # Plaintext output
        tk.Label(self.root, text="Plaintext:").pack(anchor="w")
        self.plain_output = tk.Text(self.root, height=10, width=100, state=tk.NORMAL)
        self.plain_output.pack()
        self.plain_output.tag_config("diff", foreground="red")

        # Frequency graph
        self.figure, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

    def on_ciphertext_change(self, event=None):
        self.ciphertext = self.cipher_input.get("1.0", tk.END).upper()
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
        reverse_map = {}
        for cipher_letter, var in self.mapping_vars.items():
            val = var.get().upper()
            if val in string.ascii_uppercase and val not in reverse_map.values():
                reverse_map[cipher_letter] = val
            else:
                reverse_map[cipher_letter] = ''

        for k, v in reverse_map.items():
            self.mapping[k] = v if v in string.ascii_uppercase else '?'

        self.update_plaintext()
        self.update_graph()

    def update_plaintext(self):
        self.plain_output.config(state=tk.NORMAL)
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.tag_remove("diff", "1.0", tk.END)

        line_start = 1
        for line in self.ciphertext.splitlines():
            translated_line = ''.join(
                self.mapping.get(char, char) if char in string.ascii_uppercase else char
                for char in line
            )
            self.plain_output.insert(f"{line_start}.0", translated_line + "\n")

            for i, (c_char, p_char) in enumerate(zip(line, translated_line)):
                if c_char != p_char:
                    tag_start = f"{line_start}.{i}"
                    tag_end = f"{line_start}.{i+1}"
                    self.plain_output.tag_add("diff", tag_start, tag_end)

            line_start += 1

        self.plain_output.config(state=tk.DISABLED)

    def update_graph(self, source_text=None):
        self.ax.clear()
        if source_text is None:
            source_text = self.ciphertext

        counts = Counter(c for c in source_text if c in string.ascii_uppercase)
        letters = list(string.ascii_uppercase)
        freqs = [counts.get(letter, 0) for letter in letters]

        self.ax.bar(letters, freqs, color='skyblue')
        self.ax.set_title("Letter Frequency")
        self.ax.set_ylabel("Frequency")
        self.ax.set_xlabel("Letter")
        self.figure.tight_layout()
        self.canvas.draw()

    def analyze_plaintext(self):
        self.plain_output.config(state=tk.NORMAL)
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.tag_remove("diff", "1.0", tk.END)
        self.ax.clear()
        self.canvas.draw()

        # Apply mapping
        translated_lines = []
        for line in self.ciphertext.splitlines():
            translated_line = ''.join(
                self.mapping.get(char, char) if char in string.ascii_uppercase else char
                for char in line
            )
            translated_lines.append(translated_line)

        plaintext = "\n".join(translated_lines)

        # Display resulting plaintext with red highlighting
        line_start = 1
        for cipher_line, plain_line in zip(self.ciphertext.splitlines(), translated_lines):
            self.plain_output.insert(f"{line_start}.0", plain_line + "\n")
            for i, (c_char, p_char) in enumerate(zip(cipher_line, plain_line)):
                if c_char != p_char:
                    tag_start = f"{line_start}.{i}"
                    tag_end = f"{line_start}.{i+1}"
                    self.plain_output.tag_add("diff", tag_start, tag_end)
            line_start += 1

        self.plain_output.config(state=tk.DISABLED)

        # Frequency analysis on plaintext
        self.update_graph(source_text=plaintext)

    def on_close(self):
        print("Closing application gracefully...")
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SubstitutionCipherApp(root)
    root.mainloop()

