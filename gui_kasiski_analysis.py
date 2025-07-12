#!/usr/bin/python3
import tkinter as tk
from collections import defaultdict


def prime_factors(n):
    """Return the list of prime factors of a positive integer n."""
    factors = []
    if n <= 1:
        return factors  # No prime factors for 1 or non-positive numbers

    # Check for divisibility by 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd numbers from 3 up to sqrt(n)
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            factors.append(factor)
            n //= factor
        factor += 2

    # If remainder is a prime number > 2
    if n > 1:
        factors.append(n)

    return factors


class PatternAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Exact Repeated Pattern Highlighter")

        self.textbox = tk.Text(root, height=30, width=100, wrap=tk.WORD)
        self.textbox.pack(padx=10, pady=10)

        self.analyze_button = tk.Button(root, text="Analyze", command=self.analyze)
        self.analyze_button.pack(pady=5)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=5)

        self.patterns_by_length = {}
        self.tags_used = []
        self.text_no_newlines = ""
        self.index_map = []  # Maps clean string index to Text widget index

        self.colors = [
            "yellow", "light green", "light blue", "orange", "peach puff"
        ]

    def analyze(self):
        self.clear_tags()
        full_text = self.textbox.get("1.0", tk.END)

        # Build cleaned text and index map (skip newlines)
        self.text_no_newlines = ""
        self.index_map = []
        row, col = 1, 0

        for ch in full_text:
            index_str = f"{row}.{col}"
            if ch != '\n':
                self.text_no_newlines += ch
                self.index_map.append(index_str)
                col += 1
            else:
                row += 1
                col = 0

        # Build patterns
        self.patterns_by_length.clear()
        for length in range(3, 8):
            pattern_positions = defaultdict(list)
            for i in range(len(self.text_no_newlines) - length + 1):
                pattern = self.text_no_newlines[i:i + length]
                pattern_positions[pattern].append(i)

            repeated = {k: v for k, v in pattern_positions.items() if len(v) > 1}
            self.patterns_by_length[length] = repeated

        self.create_length_buttons()

    def create_length_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for length in sorted(self.patterns_by_length.keys()):
            tk.Button(self.buttons_frame, text=f"Length {length}",
                      command=lambda l=length: self.highlight_repeats(l)).pack(side=tk.LEFT, padx=5)

    def highlight_repeats(self, length):
        self.clear_tags()
        repeated = self.patterns_by_length.get(length, {})
        color_index = 0

        #for pattern, positions in repeated.items():
        for pattern, positions in sorted(repeated.items(), key=lambda x: len(x[1]), reverse=True):
            color = self.colors[color_index]
            tag_name = f"pattern_{color_index}"
            self.textbox.tag_config(tag_name, background=color)

            offset_str = ''
            prev_pos = 0
            for pos in positions:
                if prev_pos != 0:
                    x = ' '.join(map(str, prime_factors(pos-(prev_pos+length))))
                    offset_str += ' '+str(pos-(prev_pos+length))+' ('+x+')'
                if pos + length > len(self.index_map):
                    continue  # Skip if beyond available characters

                start_idx = self.index_map[pos]
                end_idx = self.index_map[pos + length - 1]

                # Convert start and end index to "line.char" format
                self.textbox.tag_add(tag_name, start_idx, self._next_char(end_idx))
                prev_pos = pos
            print( pattern+': '+str(len(positions))+'    '+offset_str+'    '+self.colors[color_index] )
            self.tags_used.append(tag_name)
            color_index += 1
            if color_index >= len( self.colors ):
                break
        print( '-----' )

    def _next_char(self, index_str):
        """Get the next character index in Text widget after index_str"""
        line, col = map(int, index_str.split('.'))
        return f"{line}.{col + 1}"

    def clear_tags(self):
        for tag in self.tags_used:
            self.textbox.tag_remove(tag, "1.0", tk.END)
            self.textbox.tag_delete(tag)
        self.tags_used.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = PatternAnalyzer(root)
    root.mainloop()

