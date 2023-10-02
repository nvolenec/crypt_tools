import re
import argparse
import sys
import os
import subprocess
import caeser
import freq_analysis

def char_range( c1, c2 ):
    rtn = []
    for a in range( ord(c1), ord(c2)+1 ):
        rtn.append( chr(a) )
    return rtn

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
    best_match = [0]

    #run chars in text, if all 1's and 0's, if all numbers, if characters
    freq_analysis = freq_analysis.do_freq_count(input_txt)
    fa_keys = sorted( freq_analysis.keys() )
    fa_keys_s = set( fa_keys )
    print( fa_keys )
    print ( '--------' )
    print( char_range('0','7') )
    #type = 'unknown'
    #if fa_keys_s.issubset( ['0','1',' '] ):
    #    type = 'bin'
    #elif fa_keys_s.issubset( char_range( '0','7' ).append( ' ' ) ):
    #    type = 'oct'
    #elif fa_keys_s.issubset( char_range( '0','9' ).append( ' ' ) ):
    #    type = 'dec'
    #elif fa_keys_s.issubset( char_range( '0','9' ).append( char_range( 'A','F' ) ).append( ' ' ) ):
    #    type = 'hex'
    #elif fa_keys_s.issubset( char_range( '0','9' ).append( char_range( 'A','Z' ) ).append( char_range( 'a','z' ) ).append( ' ' ) ):
    #    type = 'normal'
    #elif fa_keys_s.issubset( char_range( '0','9' ).append( char_range( 'A','Z' ) ).append( char_range( 'a','z' ) ).append( ['+','/','='] ) ):
    #    type = 'base64'
                


    #if in base64 charset only, try base64
    #if characters check for spaces, if none, take note or a space every x chars then try word matching on plaintext
    for a in range(1,25):
        #if args.verbose:
        #    print( 'echo "{}" | python3.11 ./caeser.py - {} {}'.format( input_txt, a, case_s )  )
        output = caeser.do_caeser( input_txt, a )
        #a_str = str(a)
        #input_utf8 = input_txt.encode('utf-8')
        #result = subprocess.run( ['python3.11', './caeser.py', '-', a_str ], stdout=subprocess.PIPE, input=input_utf8 )
        #decrypt_try = result.stdout.decode('utf-8')
        #decrypt_try_lines = decrypt_try.splitlines()
        #print( len(decrypt_try_lines) )
        #print( decrypt_try_lines[0] )
        #print( decrypt_try_lines[1] )
        decrypt_try_utf8 = output.encode('utf-8')
        match_results = subprocess.run( ['python3.11', '/home/nvolenec/crypt_tools/dict_search.py', '-'], stdout=subprocess.PIPE, input=decrypt_try_utf8 )
        dict_search_out = match_results.stdout.decode('utf-8')
        dict_search_out_lines = dict_search_out.splitlines()
        #print( 'dict_search: {}'.format( len(dict_search_out_lines) ) )
        #print( dict_search_out_lines[0] )
        #print( dict_search_out_lines[1] )
        #print( dict_search_out_lines[2] )
        #print( dict_search_out_lines[3] )
        m = re.match( r"\W+(\d+) matches of (\d+) chars, ([0-9.]+)%", dict_search_out_lines[3] )
        if  int(m.group(1)) > best_match[0]:
            best_match = [ int(m.group(1)), 'caeser {}'.format(a), output, dict_search_out_lines[1] ]
        #print( '{} of {}  -> {}%'.format( m.group(1), m.group(2), m.group(3) ) )
        #print( '----' )
        #print( result.stdout.decode('utf-8') )
    #try atbash
    print( '{}\n{}\n{}\n'.format(best_match[1], best_match[2], best_match[3] ) )


