import re
import argparse


def process_args( ):
    parser = argparse.ArgumentParser( prog="chars_in_txt",
                                      description="outputs a list of the character space of the input file" )
    parser.add_argument( "input_file" )
    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    f = open( file_to_read, "r" )
    return f


def chars_content( input_str ):
    chars= []
    for char in input_str:
        if char not in ['\n']:
            if char not in chars:
                chars.append(char)
    return chars


if __name__ == "__main__":
    args = process_args()
    input_file = load_file( args.input_file )
    input_txt = input_file.read()
    chars = chars_content( input_txt )
    print( chars )
        


