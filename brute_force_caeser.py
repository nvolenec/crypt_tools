import re
import argparse
import sys
import os
import subprocess
import caeser


def process_args( ):
    parser = argparse.ArgumentParser( prog="Brute Forcer",
                                      description="give me some ciphertext and yo I'll solve it" )
    parser.add_argument( "input_file" )
    parser.add_argument( "-c", "--case-sensitive", action='store_true' )
    parser.add_argument( "-v", "--verbose", action='store_true' )
    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    if file_to_read == "-":
        input_txt = sys.stdin.read()
    else:
        f = open( file_to_read, "r" )
        input_txt = f.read()
    return input_txt


if __name__ == "__main__":
    args = process_args()
    input_txt = load_file( args.input_file )
    input_txt = input_txt.rstrip()
    case_s = ''
    if args.case_sensitive:
        case_s = '-c'
    for a in range(1,25):
        #if args.verbose:
        #    print( 'echo "{}" | python3.11 ./caeser.py - {} {}'.format( input_txt, a, case_s )  )
        output = caeser.do_caeser( input_txt, a )
        print( output )
        #a_str = str(a)
        #input_utf8 = input_txt.encode('utf-8')
        #result = subprocess.run( ['python3.11', './caeser.py', '-', a_str ], stdout=subprocess.PIPE, input=input_utf8 )
        #output = result.stdout.decode('utf-8')
        #output_lines = output.splitlines()
        #print( len(output_lines) )
        #print( output_lines[0] )
        #print( output_lines[1] )
        #print( result.stdout.decode('utf-8') )


