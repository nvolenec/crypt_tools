#!/usr/bin/python3
import argparse
import string
import itertools
from dict import Dict

#TODO: maybe make permutation search smarter, start with shorter permutations then prune from full list of permutations of length 10--not sure how

def process_args():
    parser = argparse.ArgumentParser( prog='monoalpha_sub_solver',
                                      description='tries to brute force monoalphabet subsitution cipher' )
    parser.add_argument( 'ciphertext_file' )
    parser.add_argument( '-r', '--respect_spaces', action='store_true' )
    parser.add_argument( '-f', '--use_freq_analysis', action='store_true' )
    parser.add_argument( '-w', '--word-guess' )
    parser.add_argument( '-s', '--searchspace', type=int )
    parser.add_argument( '-d', '--dict' )

    args = parser.parse_args()
    return args

def word_profile( word ):
    seen = []
    new_word = ''
    counter = 1
    for l in word:
        if l in seen:
            new_word += str(seen.index(l)+1)
        else:
            new_word += str(counter)
            seen.append(l)
            counter += 1
    return new_word

if __name__ == "__main__":
    args = process_args()
    with open( args.ciphertext_file, 'r' ) as f:
        ciphertext = f.read().lower()
    respect_spaces = args.respect_spaces
    if len(ciphertext ) > 180:
        print( ciphertext[0:180]+'...' )
    else:
        print( ciphertext )
    if respect_spaces:
        #remove whitespace but keep original so they can be displayed in output
        words = ciphertext.split()


    permutations = itertools.permutations( range(0,10) )
    ciphertext_segments = int( min( len(ciphertext)/10, 120/10) )
    for key_try in permutations:
        if key_try != range(0,10):
            plaintext_try = []
            #print( 'key_try' )
            #print( key_try )
            for x in range(0,ciphertext_segments):
                c = 0
                for a in key_try:
                    # [x*10+c] <- [x*10+a]
                    #print( '['+str(x)+'*10+'+str(c)+'] '+ str(x*10+c)+' <- ['+str(x)+'*10+'+str(a)+'] '+ str(x*10+a) )
                    plaintext_try.append( ciphertext[x*10+a] )
                    c += 1
            plaintext_try_s = ''.join(plaintext_try)
            #print( plaintext_try_s )
            match_dict = Dict( 'google_and_lewis_carroll_dict.txt-sorted-no_1_lett', split_by_first_let=1 )
            if respect_spaces:
                match_text = match_dict.match_vs_dict( plaintext_try_s, 1 )
            else:
                match_text = match_dict.match_vs_dict( plaintext_try_s, 0 )

            if len(ciphertext) > 180:
                ciphertext_short = ciphertext[0:180]
            else:
                ciphertext_short = ciphertext
            count_ignore_chars = ciphertext_short.count(' ') + ciphertext_short.count('.') + ciphertext_short.count(',') + ciphertext_short.count('\'')
            no_match_count = match_text.count('~') - count_ignore_chars
            t1 = len(ciphertext_short)-count_ignore_chars
            percent = ((t1-no_match_count)/t1)*100
            if percent > 70:
                print( 'key_try' )
                print( key_try )
                print( 'match_text' )
                print( match_text )
                print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent)+'%' )


            




