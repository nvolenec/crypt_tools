#!/usr/bin/python3
import argparse
import itertools
from dict import Dict
import match_vs_dict
import re
import threading
import time
import random
import freq_analysis

random.seed()

def process_args():
    parser = argparse.ArgumentParser( prog='monoalpha_sub_solver',
                                      description='tries to brute force monoalphabet subsitution cipher' )
    parser.add_argument( 'ciphertext_file' )
    #parser.add_argument( '-w', '--keyword' )
    #parser.add_argument( '-d', '--dict' )
    #parser.add_argument( '--slice', type=str )
    #parser.add_argument( '-t', '--threads', nargs='?', const=1, type=int, default=8 )
    parser.add_argument( '--respect_spaces', action='store_true' )
    parser.add_argument( '--use_freq_analysis', action='store_true' )
    parser.add_argument( '-w', '--word-guess' )
    args = parser.parse_args()
    return args

def gen_subsitution_alphabet( ):
    alpha = ''
    for i in range(0,25):
        t = chr( random.randint(0,25)+65)
        while t in alpha:
            t = chr(((ord(t)-65+1)%26)+65)
        alpha += t

    #last char
    t = chr(((ord(t)-65+1)%26)+65)
    while t in alpha:
        t = chr(((ord(t)-65+1)%26)+65)
    alpha += t
    as_ints = []
    for a in alpha:
        as_ints.append( ord(a)-65 )
    return (alpha, as_ints)

# implementation licensed under BSD https://github.com/toastdriven/pylev
def recursive_levenshtein( string_1, string_2, len_1=None, len_2=None, offset_1=0, offset_2=0, memo=None):
    
    if len_1 is None:
        len_1 = len(string_1)
    if len_2 is None:
        len_2 = len(string_2)
    if memo is None:
        memo = {}

    key = ",".join([str(offset_1), str(len_1), str(offset_2), str(len_2)])

    if memo.get(key) is not None:
        return memo[key]

    if len_1 == 0:
        return len_2
    elif len_2 == 0:
        return len_1

    cost = 0

    if string_1[offset_1] != string_2[offset_2]:
        cost = 1

    dist = min(
        recursive_levenshtein( string_1, string_2, len_1 - 1, len_2, offset_1 + 1, offset_2, memo) + 1,
        recursive_levenshtein( string_1, string_2, len_1, len_2 - 1, offset_1, offset_2 + 1, memo) + 1,
        recursive_levenshtein( string_1, string_2, len_1 - 1, len_2 - 1, offset_1 + 1, offset_2 + 1, memo) + cost,
    )
    memo[key] = dist
    return dist


def decrypt( ciphertext, keyword ): #keyword is a 26 char word 
    plaintext = ''
    for char_x in ciphertext:
        char_idx = ord(char_x)-97
        if char_idx >= 0 and char_idx < 26:
            plaintext += keyword[char_idx]
    return plaintext


if __name__ == "__main__":
    args = process_args()
    with open( args.ciphertext_file, 'r' ) as f:
        ciphertext = f.read().lower()
    respect_spaces = args.respect_spaces
    word_guess = args.word_guess:
    words = []
    if respect_spaces:
        words = ciphertext.split()

    if respect_spaces and word_guess:
        #check for words that match the length of the guess word
        len_matches = {}
        for word in words:
            if len(word) == len(word_guess)
                if word not in len_matches:
                    len_matches[word] = ''
        print( 'there are '+len(len_matches)+' word of the same length as '+word_guess )
    if args.use_freq_analysis:
        freq_analysis = freq_analysis.do_freq_count( ciphertext)


    #TODO:before doing any analysis run ioc and kasski examination 

    print( ciphertext )
    plaintext = ''
    if args.keyword is not None:
        keyword = args.keyword.lower()
        print( keyword )
        plaintext = vigenere_decrypt( ciphertext, keyword )
        print(plaintext)
    elif args.length is not None:
        #first try all words in dict file of length args.length
        if dictfile:
            dict = Dict(dictfile)
        else:
            dict = Dict()
        word_list = dict.get_words_of_len( int(args.length) )
        #word_list = get_from_dict.get_words_of_len( int(args.length) )
        word_list_sz = len( word_list )
        print( str(word_list_sz)+' words of length '+args.length )
        if args.use_freq_analysis:   #don't do raw brute force run freq_analysis and generate random keys similar to the
                                     #frequencey analysis
            ciphertext_split = ciphertext.split()
            ciphertext_split_len = []
            ciphertext_split_offset = [] #does not count spaces
            sum = 0
            for w in ciphertext_split:
                ciphertext_split_len.append( len( w ) )
                ciphertext_split_offset.append( sum )
                sum += len(w)
            one_letter_word_indx = []
            iterator_input_list = []
            pos = 0
            text_mask = ''
            for index, value in enumerate( ciphertext_split_len ):
                if value == 1:   #find 1 letter words
                    one_letter_word_indx.append(pos)
                    iterator_input_list.append( ['a','i'] )
                    text_mask += 'X'
                else:
                    pos += value
                    text_mask += '~' * value
            enum_one_letter_words = []
            
            all_possible_one_letter_word_combos = list( itertools.product( ['a','i'], repeat=len(one_letter_word_indx) ) )

            key_mask_try = ''
            first = 1
            print( all_possible_one_letter_word_combos )
            print( all_possible_one_letter_word_combos[0] )
            print( ciphertext )
            print( ciphertext_no_spaces )
            print( text_mask )
            one_letter_word_offsets = []
            first = 1
            for a in all_possible_one_letter_word_combos:
                #print( a )
                #key_mask_try = text_mask
                key_mask_try = ''
                counter = 0
                for i, c in enumerate(text_mask):
                    if c == '~':
                        key_mask_try += '~'
                    if c == 'X':
                        if first:
                            one_letter_word_offsets.append( i )
                        #print( counter )
                        #key_mask_try += a[counter]
                        key_mask_try += chr(((ord(ciphertext_no_spaces[i])-97) - (ord(a[counter])-97))%26+97)
                        counter += 1
                        #print( key_mask_try )
                first = 0
                print( key_mask_try )
                guess_keys = try_key_length( int(args.length), one_letter_word_offsets, key_mask_try, dictfile )
                if guess_keys:
                    print( guess_keys )
                    for guess_key in guess_keys:
                        guess_plaintext = vigenere_decrypt( ciphertext, guess_key )
                        match_text = match_vs_dict.match_vs_dict( guess_plaintext, 1 )
                        #print( guess_plaintext )
                        print( match_text )
                        count_ignore_chars = ciphertext.count(' ') + ciphertext.count('.') + ciphertext.count(',') + ciphertext.count('\'')
                        no_match_count = match_text.count('~') - count_ignore_chars
                        t1 = len(ciphertext)-count_ignore_chars
                        percent = ((t1-no_match_count)/t1)*100
                        print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent)+'%' )

            print( one_letter_word_offsets )

        else:  #have length but not smart, raw brute force key try
            counter = 1 
            for word in word_list:
                #if counter % 100 == 0:
                #    print( str(counter) )
                guess_plaintext = vigenere_decrypt( ciphertext, word )
                match_text = match_vs_dict.match_vs_dict( guess_plaintext, 1 )
                #print( guess_plaintext )
                count_ignore_chars = ciphertext.count(' ') + ciphertext.count('.') + ciphertext.count(',') + ciphertext.count('\'')
                no_match_count = match_text.count('~') - count_ignore_chars
                t1 = len(ciphertext)-count_ignore_chars
                percent = ((t1-no_match_count)/t1)*100
                if percent > 50:
                    print( 'key: '+word )
                    print( match_text )
                    print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent)+'%' )
                counter += 1

            #print( one_letter_word_offsets )

    else: #bruteforce without length -- this assumes key is a single word
        if dictfile:
            key_dict = Dict(dictfile)
        else:
            key_dict = Dict()
        word_dict = Dict( split_by_first_let=1)
        key_list = key_dict.get_dict()
        counter = 1
        match_count = 0
        if args.slice:   #expecting input of the format 1/16, 5/32, 10/10, etc.  1-indexed
            (s, t) = args.slice.split( '/', 2 )
            threadcount = int(t)
            segment = int(s)
            print( s+'/'+t )
        else:
            threadcount=args.threads
        split_key_lists = []
        b= 0
        part = len(key_list) / threadcount
        for a in range(1,threadcount+1):
            if a == threadcount:
                split_key_lists.append( key_list[b:len(key_list)] )
                #print( 'key_list['+str(b)+':'+str(len(key_list))+']' )
            else:
                split_key_lists.append( key_list[b:int(part*a)] )
                #print( 'key_list['+str(b)+':'+str(int(part*a))+']' )
                b = int(part*a)+1

        if args.slice:
            try_word_list( split_key_lists[segment-1], ciphertext, word_dict )
        else:
            threads = []
            for wlist_part in split_key_lists:
                t = threading.Thread(target=try_word_list, args=(wlist_part, ciphertext, word_dict) )
                threads.append(t)

            for t in threads:
                t.start()

            for t in threads:
                t.join()
            
            #if we have no good matchs after running entire dictionary we need to do something smarter
            #maybe with ioc because trying 2 word pairs will take 133 hours on my laptop. 
            #Single word run takes 1m2.3s dict file has 8,102 words


