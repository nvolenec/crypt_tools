import re
import argparse


def process_args( ):
    parser = argparse.ArgumentParser( prog="freq_analysis",
                                      description="performs a frequency analysis on an input file" )
    parser.add_argument( "input_file" )
    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    f = open( file_to_read, "r" )
    return f


def do_freq_count( input_str ):
    char_count = {}
    for char in input_str:
        if char not in ['\n']:
            if char.lower() in char_count:
                char_count[char.lower()] += 1
            else:
                char_count[char.lower()] = 1
    return {k:v for k, v in sorted(char_count.items(), key=lambda item: item[1], reverse=True)}


if __name__ == "__main__":
    args = process_args()
    input_file = load_file( args.input_file )
    input_txt = input_file.read()
    freq = do_freq_count( input_txt )
    #for k, v in resorted_freq:
    #    print( k, v )
    #for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True):
    #    print( k, v )
    #print( sorted(freq.items(), key=lambda item: item[1], reverse=True) )
    print( freq )
    #print( resorted_freq )


