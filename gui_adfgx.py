import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import Counter

ADFGX = ['A', 'D', 'F', 'G', 'X']

class ADFGXCipher:
    def __init__(self, grid_text, keyword):
        self.grid_text = grid_text.upper().replace('J', 'I')
        self.keyword = keyword.upper()
        self.grid = self.create_grid()
        self.char_to_coords = self.create_char_to_coords()
        self.coords_to_char = {v: k for k, v in self.char_to_coords.items()}

    def create_grid(self):
        cleaned = ''.join(dict.fromkeys(self.grid_text))  # Remove duplicates
        if len(cleaned) != 25:
            raise ValueError("Grid must contain 25 unique characters.")
        return [list(cleaned[i:i+5]) for i in range(0, 25, 5)]

    def create_char_to_coords(self):
        mapping = {}
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                mapping[char] = ADFGX[i] + ADFGX[j]
        return mapping

    def polybius_encrypt(self, plaintext):
        plaintext = plaintext.upper().replace('J', 'I')
        return ''.join(self.char_to_coords[char] for char in plaintext if char in self.char_to_coords)

    def polybius_decrypt(self, cipher_pairs):
        return ''.join(self.coords_to_char.get(pair, '?') for pair in cipher_pairs)

    def columnar_transposition(self, text):
        n = len(self.keyword)
        columns = ['' for _ in range(n)]
        for i, char in enumerate(text):
            columns[i % n] += char

        key_order = sorted(list(enumerate(self.keyword)), key=lambda x: x[1])
        transposed = ''.join(columns[i] for i, _ in key_order)
        return transposed

    def columnar_decryption(self, text):
        n = len(self.keyword)
        length = len(text)
        col_lengths = [length // n] * n
        for i in range(length % n):
            col_lengths[i] += 1

        key_order = sorted(list(enumerate(self.keyword)), key=lambda x: x[1])
        columns = ['' for _ in range(n)]

        index = 0
        for (orig_idx, _), l in zip(key_order, col_lengths):
            columns[orig_idx] = text[index:index+l]
            index += l

        decrypted = ''
        for i in range(max(col_lengths)):
            for col in columns:
                if i < len(col):
                    decrypted += col[i]
        return decrypted

    def encrypt(self, plaintext):
        polybius = self.polybius_encrypt(plaintext)
        return self.columnar_transposition(polybius)

    def decrypt(self, ciphertext):
        polybius = self.columnar_decryption(ciphertext)
        pairs = [polybius[i:i+2] for i in range(0, len(polybius), 2)]
        return self.polybius_decrypt(pairs)

    @staticmethod
    def bigram_analysis(ciphertext):
        bigrams = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        return Counter(bigrams)


class ADFGXApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGX Cipher GUI")
        self.root.geometry("600x600")
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def create_widgets(self):
        tk.Label(root, text="ADFGX Grid (25 letters A-Z, no J):").pack()
        self.grid_entry = tk.Entry(root, width=30)
        self.grid_entry.insert(0, "PHQGMEAYNOFDXKRCVSTZWBULI")  # Default grid
        self.grid_entry.pack()

        tk.Label(root, text="Permutation Keyword:").pack()
        self.key_entry = tk.Entry(root, width=30)
        self.key_entry.insert(0, "KEYWORD")  # Default keyword
        self.key_entry.pack()

        tk.Label(root, text="Plaintext:").pack()
        self.plain_entry = tk.Entry(root, width=50)
        self.plain_entry.pack()

        tk.Label(root, text="Ciphertext:").pack()
        self.cipher_entry = tk.Entry(root, width=50)
        self.cipher_entry.pack()

        tk.Button(root, text="Encrypt", command=self.encrypt).pack(pady=5)
        tk.Button(root, text="Decrypt", command=self.decrypt).pack(pady=5)
        tk.Button(root, text="Bigram Analysis", command=self.analyze_bigrams).pack(pady=5)

        tk.Label(root, text="Output:").pack()
        self.output_box = scrolledtext.ScrolledText(root, width=70, height=15)
        self.output_box.pack()

    def encrypt(self):
        try:
            cipher = ADFGXCipher(self.grid_entry.get(), self.key_entry.get())
            plaintext = self.plain_entry.get()
            result = cipher.encrypt(plaintext)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, f"Ciphertext: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        try:
            cipher = ADFGXCipher(self.grid_entry.get(), self.key_entry.get())
            ciphertext = self.cipher_entry.get()
            result = cipher.decrypt(ciphertext)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, f"Plaintext: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def analyze_bigrams(self):
        ciphertext = self.cipher_entry.get().upper()
        if not ciphertext:
            messagebox.showinfo("Info", "Please enter ciphertext for analysis.")
            return
        analysis = ADFGXCipher.bigram_analysis(ciphertext)
        output = "\n".join(f"{k}: {v}" for k, v in analysis.most_common())
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"Bigram Frequency:\n{output}")

    def on_exit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ADFGXApp(root)
    root.mainloop()

