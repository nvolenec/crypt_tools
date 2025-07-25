import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import string

ADFGX_ALPHABET = 'ADFGX'

class ADFGXCipher:
    def __init__(self, grid_key, keyword):
        self.grid_key = self.prepare_grid(grid_key)
        self.keyword = keyword.upper()

    def prepare_grid(self, key):
        key = ''.join(dict.fromkeys(key.upper().replace('J', 'I')))  # Remove duplicates
        alphabet = ''.join([ch for ch in string.ascii_uppercase if ch != 'J'])
        for ch in alphabet:
            if ch not in key:
                key += ch
        return key

    def encrypt(self, plaintext):
        plaintext = plaintext.upper().replace('J', 'I')
        coords = self.get_polybius_coordinates(plaintext)
        transposed = self.columnar_transpose(coords, self.keyword)
        return transposed

    def decrypt(self, ciphertext):
        coords = self.inverse_columnar_transpose(ciphertext, self.keyword)
        plaintext = self.get_plaintext_from_coordinates(coords)
        return plaintext

    def get_polybius_coordinates(self, text):
        coords = ''
        for ch in text:
            if ch in self.grid_key:
                idx = self.grid_key.index(ch)
                row = idx // 5
                col = idx % 5
                coords += ADFGX_ALPHABET[row] + ADFGX_ALPHABET[col]
        return coords

    def get_plaintext_from_coordinates(self, coords):
        text = ''
        for i in range(0, len(coords), 2):
            try:
                row = ADFGX_ALPHABET.index(coords[i])
                col = ADFGX_ALPHABET.index(coords[i+1])
                index = row * 5 + col
                text += self.grid_key[index]
            except (IndexError, ValueError):
                continue
        return text

    def columnar_transpose(self, text, keyword):
        cols = {k: '' for k in sorted(set(keyword))}
        for i, ch in enumerate(text):
            cols[keyword[i % len(keyword)]] += ch
        return ''.join(cols[k] for k in sorted(cols))

    def inverse_columnar_transpose(self, text, keyword):
        n = len(keyword)
        col_lens = [len(text) // n + (1 if i < len(text) % n else 0) for i in range(n)]
        sorted_keyword = sorted([(ch, i) for i, ch in enumerate(keyword)])
        cols = {}
        index = 0
        for ch, i in sorted_keyword:
            cols[i] = text[index:index+col_lens[i]]
            index += col_lens[i]
        out = ''
        for i in range(max(col_lens)):
            for j in range(n):
                if i < len(cols[j]):
                    out += cols[j][i]
        return out

    def bigram_analysis(self, text):
        bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
        return dict(Counter(bigrams))

class ADFGXApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGX Cipher Tool")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.setup_widgets()

    def setup_widgets(self):
        # Inputs
        ttk.Label(self.root, text="Plaintext:").grid(row=0, column=0, sticky="w")
        self.plaintext_entry = tk.Text(self.root, height=4, width=50)
        self.plaintext_entry.grid(row=1, column=0, columnspan=2)

        ttk.Label(self.root, text="Ciphertext:").grid(row=2, column=0, sticky="w")
        self.ciphertext_entry = tk.Text(self.root, height=4, width=50)
        self.ciphertext_entry.grid(row=3, column=0, columnspan=2)

        ttk.Label(self.root, text="Grid Key (25 letters):").grid(row=4, column=0, sticky="w")
        self.grid_entry = ttk.Entry(self.root, width=50)
        self.grid_entry.grid(row=5, column=0, columnspan=2)

        ttk.Label(self.root, text="Keyword (permutation):").grid(row=6, column=0, sticky="w")
        self.keyword_entry = ttk.Entry(self.root, width=50)
        self.keyword_entry.grid(row=7, column=0, columnspan=2)

        # Buttons
        ttk.Button(self.root, text="Encrypt", command=self.encrypt).grid(row=8, column=0, pady=10)
        ttk.Button(self.root, text="Decrypt", command=self.decrypt).grid(row=8, column=1)

        # Bigrams output
        ttk.Label(self.root, text="Bigram Analysis:").grid(row=9, column=0, sticky="w")
        self.bigram_output = tk.Text(self.root, height=6, width=50, state='disabled')
        self.bigram_output.grid(row=10, column=0, columnspan=2)

    def encrypt(self):
        plaintext = self.plaintext_entry.get("1.0", "end").strip()
        grid = self.grid_entry.get().strip()
        keyword = self.keyword_entry.get().strip()

        if not (plaintext and grid and keyword):
            messagebox.showerror("Missing Input", "Please fill all fields.")
            return

        cipher = ADFGXCipher(grid, keyword)
        ciphertext = cipher.encrypt(plaintext)
        self.ciphertext_entry.delete("1.0", "end")
        self.ciphertext_entry.insert("1.0", ciphertext)
        self.display_bigrams(cipher.bigram_analysis(ciphertext))

    def decrypt(self):
        ciphertext = self.ciphertext_entry.get("1.0", "end").strip()
        grid = self.grid_entry.get().strip()
        keyword = self.keyword_entry.get().strip()

        if not (ciphertext and grid and keyword):
            messagebox.showerror("Missing Input", "Please fill all fields.")
            return

        cipher = ADFGXCipher(grid, keyword)
        plaintext = cipher.decrypt(ciphertext)
        self.plaintext_entry.delete("1.0", "end")
        self.plaintext_entry.insert("1.0", plaintext)
        self.display_bigrams(cipher.bigram_analysis(ciphertext))

    def display_bigrams(self, bigrams):
        self.bigram_output.config(state='normal')
        self.bigram_output.delete("1.0", "end")
        for k, v in sorted(bigrams.items()):
            self.bigram_output.insert("end", f"{k}: {v}\n")
        self.bigram_output.config(state='disabled')

    def on_exit(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ADFGXApp(root)
    root.mainloop()

