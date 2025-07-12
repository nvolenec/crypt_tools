import string
import sys
import os

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python ic_calculator.py <ciphertext_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        ciphertext = f.read()

    ic = index_of_coincidence(ciphertext)
    print(f"Index of Coincidence: {ic:.5f}")

if __name__ == "__main__":
    main()

