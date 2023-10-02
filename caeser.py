import re
import argparse
import sys

def process_args( ):
    parser = argparse.ArgumentParser( prog="Casesar crypto tool",
                                      description="Loads a file and performs the specified Caeser encrpytion" )
    parser.add_argument( "input_file" )
    parser.add_argument( "offset" )
    parser.add_argument( "-c", "--case-sensitive", action="store_true" )
    parser.add_argument( "-v", "--verbose", action="store_true" )
    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    if file_to_read == '-':
        input_txt = sys.stdin.read()
    else:
        f = open( file_to_read, "r" )
        input_txt = f.read()
    return input_txt 

def do_caeser( input_txt, offset ):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    running_txt = ''
    #running_txt_flip = ''
    for char in input_txt:
        #char_flip = char
        pos = alphabet.find(char)
        if pos != -1:
            char = alphabet[(pos+offset)%26]
            #char_flip = alphabet[(pos+26-offset)%26]
        else:
            pos = alphabet_u.find(char)
            if pos != -1:
                char = alphabet_u[(pos+offset)%26]
                #char_flip = alphabet_u[(pos+26-offset)%26]
        running_txt += char
        #running_txt_flip += char_flip
    return running_txt



if __name__ == "__main__":
    args = process_args()
    input_txt = load_file( args.input_file )
    offset = int( args.offset )
    running_txt = do_caeser( input_file, offset )

    print( "<- {} (->{})".format(offset, 26-offset) )
    print( running_txt )
    #if args.verbose:
    #    print( "\n-> {} (<-{})".format( 26-offset, offset) )
    #    print( running_txt_flip )


