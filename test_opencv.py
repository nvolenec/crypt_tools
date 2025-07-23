import cv2
import numpy as np
import argparse

def detect_symbols(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 127,255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    symbols = []

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if h > w*3:
            symbols.append('|')
        elif w > h*2:
            symbols.append('-')
        else:
            symbols.append('?')

    sorted_symbols = sorted(zip(contours, symbols), key=lambda item: cv2.boundingRect(item[0])[0])
    output = ''.join(sym for _, sym in sorted_symbols)
    return output
 
parser = argparse.ArgumentParser("openCV test")
parser.add_argument('input_file', help='image file to process', type=str)
args = parser.parse_args()

result = detect_symbols(args.input_file)
print( 'Detected symbols:', result)

