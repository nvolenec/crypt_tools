#!/usr/bin/python3
import argparse
import string
import dict
import calc_ioc
import freq_analysis
import english_letter_freq as elf
from collections import Counter


def process_args():
    parser = argparse.ArgumentParser( prog='monoalpha_first_pass',
                                      description='quick decryptor that tries caesar shifts and reverse alphabet' )
    parser.add_argument( 'ciphertext_file' )
    parser.add_argument( '-d', '--dict' )

    args = parser.parse_args()
    return args


def decrypt( ciphertext, keyword ): #keyword is a list of 26 ints
    plaintext = ''
    for char_x in ciphertext:
        char_idx = ord(char_x)-97
        if char_idx >= 0 and char_idx < 26:
            #print( char_x+'('+str(char_idx)+') => '+chr(keyword[char_idx]+97)+'('+str(keyword[char_idx])+')' )
            plaintext += chr(keyword[char_idx]+97)
        else:
            #print( str(char_idx)+' out of range' )
            plaintext += char_x
    return plaintext


if __name__ == "__main__":
    args = process_args()
    with open( args.ciphertext_file, 'r' ) as f:
        ciphertext = f.read()
    ciphertext_low = ciphertext.lower()
    if len(ciphertext ) > 180:
        print( ciphertext[0:180]+'...' )
    else:
        print( ciphertext )

    cc = Counter(ciphertext)
    cc_low = Counter(ciphertext_low)
    ioc = calc_ioc.index_of_coincidence( ciphertext_low )
    print( "IOC: {:.4f}  {} unique chars, {} unique case insensitive chars".format(ioc, len(cc),len(cc_low)) )
    ciphertext_freq_analysis = freq_analysis.do_freq_count( ciphertext_low )
    print( 'ciphertext_freq_analysis' )
    print( ciphertext_freq_analysis )
    alpha = list(range(0,26))
    alpha_rev = alpha[::-1]
    print( alpha_rev )
    alpha_caesar = []
    alpha_caesar.append( alpha )
    for a in range(1,26):
        #print( a )
        alpha_caesar.append( alpha_caesar[a-1][:] )
        alpha_caesar[a].append( alpha_caesar[a].pop(0) )
        #print( alpha_caesar[a] )


    word_dict = dict.Dict( 'google_and_lewis_carroll_dict.txt-sorted-no_1_lett', 1 )
    count_ignore_chars = ciphertext_low.count(' ') + ciphertext.count('.') + ciphertext.count(',') + ciphertext.count('\'')
    t1 = len(ciphertext_low)-count_ignore_chars
    plaintext_try = decrypt( ciphertext_low, alpha_rev )
    match_text = word_dict.match_vs_dict( plaintext_try, 0 )
    no_match_count = match_text.count('~') - count_ignore_chars
    percent = ((t1-no_match_count)/t1)*100
    if percent > 50:
        print( 'key: ' )
        print( alpha_rev )
        print( match_text )
        print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent)+'%' )

    for a in range( 1,26 ):
        plaintext_try = decrypt( ciphertext_low, alpha_caesar[a] )
        match_text = word_dict.match_vs_dict( plaintext_try, 0 )
        no_match_count = match_text.count('~') - count_ignore_chars
        percent = ((t1-no_match_count)/t1)*100
        if percent > 50:
            print( 'key: ' )
            print( alpha_caesar[a] )
            print( match_text )
            print( plaintext_try )
            print( "matched {} of {} chars, match {:.2f}%".format( (t1-no_match_count), t1, percent ))



