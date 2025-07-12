#!/usr/bin/python3
import argparse
import itertools
from dict import Dict
import match_vs_dict
import re
import threading
import time

def process_args():
    parser = argparse.ArgumentParser( prog='vigenere_solver',
                                      description='tries to solve Vigenere solver' )
    parser.add_argument( 'ciphertext_file' )
    parser.add_argument( '-l', '--length' )
    parser.add_argument( '-w', '--keyword' )
    parser.add_argument( '-d', '--dict' )
    parser.add_argument( '-t', '--threads', nargs='?', const=1, type=int, default=32 )
    parser.add_argument( '-s', '--smart', action='store_true' )
    args = parser.parse_args()
    return args

def vigenere_decrypt( ciphertext, keyword ):
    plaintext = ''
    c = 0
    for i, char_x in enumerate(ciphertext):
        if( ord(char_x) >= 97 and ord(char_x) <=122 ):
            key_char = keyword[c % len(keyword)]
            plaintext = plaintext + chr(((ord(char_x)-97) - (ord(key_char)-97))%26+97)
            #print( char_x+'('+str(ord(char_x)-97)+') + '+key_char+'('+str(ord(key_char)-97)+')')
            c = c + 1
        else:
            plaintext += char_x
    return plaintext

def try_word_list( wordlist, ciphertext ):
    output = ''
    counter = 1
    match_count = 0
    count_ignore_chars = ciphertext.count(' ') + ciphertext.count('.') + ciphertext.count(',') + ciphertext.count('\'')
    t1 = len(ciphertext)-count_ignore_chars
    for word in wordlist:
        #if counter % 100 == 0:
        #    print( str(counter) )
        guess_plaintext = vigenere_decrypt( ciphertext, word )
        match_text = match_vs_dict.match_vs_dict(guess_plaintext, 1 )
        no_match_count = match_text.count('~') - count_ignore_chars
        #percent = ((t1-no_match_count)/t1)*100
        percent = ((t1-no_match_count)/t1)
        if percent > 0.5:
            print( 'key: '+word )
            print( match_text )
            print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent*100)+'%' )
            output += 'key: '+word 
            output += match_text
            output += 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent*100)+'%' 
            match_count += 1
        counter += 1
    return output


def try_key_length( key_length, one_letter_word_offsets, key_mask_try, dictfile ):
    matching_words = []
    word_len_mask = ['.'] * key_length
    bad_key_len = False
    for d in one_letter_word_offsets:
        if word_len_mask[d%key_length]  == '.' or word_len_mask[d%key_length] == key_mask_try[d]:
            word_len_mask[d%key_length] = key_mask_try[d]
            #print( word_len_mask )
        else:
            #print( 'conflict found, key cannot be of len '+str(key_length) )
            bad_key_len = True
        #print( key_mask_try[d]+'  '+str(d%key_length) )
    if bad_key_len == False:
        word_regex = "".join(word_len_mask)
        #print( "trying to match" + word_regex )
        re_pattern = re.compile( word_regex )
        #length_dict = get_from_dict.get_words_of_len( key_length )
        if dictfile:
            dict = Dict(dictfile)
        else:
            dict = Dict()
        length_dict = dict.get_words_of_len( key_length )
        for w in length_dict:
            if re.fullmatch( re_pattern, w ) != None:
                matching_words.append( w )
    return matching_words


if __name__ == "__main__":
    args = process_args()
    f = open( args.ciphertext_file, 'r' )
    ciphertext = f.read().lower()
    ciphertext_no_spaces = ''
    dictfile = args.dict
    for a in ciphertext:
        if( ord(a) >= 97 and ord(a) <=122 ):
            ciphertext_no_spaces += a
    #before doing any analysis run ioc and kasski examination 

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
        if args.smart:
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
            #run through dictionary and see if there are any words that applied as the key
            #text_mask = ''
            #for index, a in enumerate(ciphertext):
            #    if index in one_letter_word_indx:
            #        text_mask += 'X'
            #    if( ord(a) >= 97 and ord(a) <=122 ):
            #        text_mask += '~'

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
            dict = Dict(dictfile)
        else:
            dict = Dict()
        word_list = dict.get_dict()
        #word_list = get_from_dict.get_dict_file()
        counter = 1
        match_count = 0
        #count_ignore_chars = ciphertext.count(' ') + ciphertext.count('.') + ciphertext.count(',') + ciphertext.count('\'')
        #t1 = len(ciphertext)-count_ignore_chars
        threadcount=args.threads
        split_word_lists = []
        b= 0
        part = len(word_list) / threadcount
        for a in range(1,threadcount+1):
            if a == threadcount:
                split_word_lists.append( word_list[b:len(word_list)] )
                print( 'word_list['+str(b)+':'+str(len(word_list))+']' )
            else:
                split_word_lists.append( word_list[b:int(part*a)] )
                print( 'word_list['+str(b)+':'+str(int(part*a))+']' )
                b = int(part*a)+1

        threads = []
        for wlist_part in split_word_lists:
            t = threading.Thread(target=try_word_list, args=(wlist_part, ciphertext) )
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
            
        #for word in word_list:
        #    if counter % 100 == 0:
        #        print( str(counter) )
        #    guess_plaintext = vigenere_decrypt( ciphertext, word )
        #    match_text = match_vs_dict.match_vs_dict(guess_plaintext, 1 )
        #    no_match_count = match_text.count('~') - count_ignore_chars
        #    #percent = ((t1-no_match_count)/t1)*100
        #    percent = ((t1-no_match_count)/t1)
        #    if percent > 0.5:
        #        print( 'key: '+word )
        #        print( match_text )
        #        print( 'matched '+str(t1-no_match_count)+' of '+str(t1)+' characters, match '+str(percent*100)+'%' )
        #        match_count += 1
        #    counter += 1
        #if match_count == 0: 
        #    match_count = 0
            #if we have no good matchs after running entire dictionary we need to do something smarter
            #maybe with ioc because trying 2 word pairs will take 133 hours on my laptop. 
            #Single word run takes 1m2.3s dict file has 8,102 words


