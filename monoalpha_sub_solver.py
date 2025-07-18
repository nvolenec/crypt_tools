#!/usr/bin/python3
import argparse
import string
import itertools
from dict import Dict
import match_vs_dict
import re
import threading
import time
import random
import freq_analysis
import copy
import english_letter_freq as elf

random.seed()

def process_args():
    parser = argparse.ArgumentParser( prog='monoalpha_sub_solver',
                                      description='tries to brute force monoalphabet subsitution cipher' )
    parser.add_argument( 'ciphertext_file' )
    parser.add_argument( '-r', '--respect_spaces', action='store_true' )
    parser.add_argument( '-f', '--use_freq_analysis', action='store_true' )
    parser.add_argument( '-w', '--word-guess' )
    args = parser.parse_args()
    return args

def brute_chi_sq(ciphertext_freq_analysis, ciphertext ):
    #build normalized sqared error for every letter -> letter combination, 26^2 
    c = 0
    for a in ciphertext:
        if a in string.ascii_lowercase:
            c += 1
    sum = 0.0
    norm_sq_err_dict = {}
    ordered_norm_sq_err_dict = {}
    letters_in_freq_order = [ 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u',
     'c', 'm', 'w', 'f', 'g', 'p', 'y', 'b', 'x', 'v', 'k', 'j', 'q', 'z' ]
    for a in letters_in_freq_order[::-1]:
        norm_sq_err_dict[a] = { }
        ordered_norm_sq_err_dict = {}
        for b in letters_in_freq_order[::-1]:
            x= (abs(ciphertext_freq_analysis[a] - elf.english_letter_freqs[b.upper()]*c)**2)/(elf.english_letter_freqs[b.upper()]*c)
            norm_sq_err_dict[a][b] = x

    for a in letters_in_freq_order[::-1]:
        ordered_norm_sq_err_dict[a] = dict(sorted(norm_sq_err_dict[a].items(), key=lambda item: item[1]))
    #print( '---------')
    #print( norm_sq_err_dict['e'] )
    #print( '---')
    #print( ordered_norm_sq_err_dict['e'] )
    #print( '---------')
    return ordered_norm_sq_err_dict



def chi_sq( ciphertext_freq_analysis, ciphertext ):
    c = 0
    for a in ciphertext:
        if a in ascii_lowercase:
            c += 1
    sum = 0.0
    for a in ascii_lowercase:
        sum += (abs(ciphertext_freq_analysis[a] - elf.english_letter_freqs[a.upper()])**2)/elf.english_letter_freqs[a.upper()]




def freq_diff( ciphertext_freq_analysis, ciphertext ):
    sum = 0.0
    c = 0
    for a in ciphertext:
        if a in ascii_lowercase:
            c += 1
    for lett in ascii_lowercase:
        sum += abs(ciphertext_freq_analysis[lett]/c - elf.english_letter_freqs[lett.upper()])/26
    return sum


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
        ciphertext = f.read().lower()
    respect_spaces = args.respect_spaces
    word_guess = args.word_guess
    if args.word_guess:
        word_guess = args.word_guess.lower()
        word_guess_profile = word_profile(word_guess)
        words = []
    print( ciphertext )
    if respect_spaces:
        words = ciphertext.split()

    if respect_spaces and word_guess:
        len_matches = {} #{ length: [count,[word list], [word indexs]], ... }
        unique_len_matches = {} #{ length: [count,[word list]], ... }
        for i, word in enumerate(words):
            word_len = len(word)
            if word_len  not in len_matches:
                len_matches[word_len] = [1, [word], [i]]
            else:
                #print( len_matches[word_len] )
                len_matches[word_len][0] += 1
                len_matches[word_len][1].append( word )
                len_matches[word_len][2].append( i )
        if word_guess:
            for key, val in len_matches.items():
                a = list(set(val[1]))
                unique_len_matches[key] = [len(a), a]
            to_remove = []
            for word in unique_len_matches[len(word_guess)][1]:
                if word_profile(word) != word_guess_profile:
                    print( word+'('+word_profile(word)+') incompatible with '+word_guess_profile+'('+word_guess+')')
                    to_remove.append(word)
                #else:
                #    print( word+'('+word_profile(word)+') compatible with '+word_guess_profile+'('+word_guess+')')
            for word in to_remove:
                len_matches[len(word_guess)][0] -= 1
                unique_len_matches[len(word_guess)][0] -= 1
                unique_len_matches[len(word_guess)][1].remove(word)

            #check for words that match the length of the guess word
            #if len(word) == len(word_guess):
            #    if word not in unique_len_matches:
            #        unique_len_matches[word] = ''
            print( 'there are '+str(unique_len_matches[len(word_guess)][0])+' unique words of the same length as '+word_guess+', '+str(len_matches[len(word_guess)][0])+' total' )
            print( 'len_matches' )
            print( len_matches[len(word_guess)] )
            print( 'unique_len_matches' )
            print( unique_len_matches[len(word_guess)] )

    use_case = 0
    random.seed()
    alphabet = range(0,26)
    if args.use_freq_analysis:
        ciphertext_freq_analysis = freq_analysis.do_freq_count( ciphertext )
        print( 'freq_analysis:' )
        print( ciphertext_freq_analysis )
        if respect_spaces and word_guess: 
            #placeholder 
            use_case = 1 
        elif respect_spaces: 
            ciphertext_freq_analysis = freq_analysis.do_freq_count( ciphertext )
            brute_chi_dict = brute_chi_sq( ciphertext_freq_analysis, ciphertext )
            letters_in_freq_order = { 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u',
             'c', 'm', 'w', 'f', 'g', 'p', 'y', 'b', 'x', 'v', 'k', 'j', 'q', 'z', }
            c = 0
            #while c < 26*26:
            while c < 20:
                used_list = []
                tmp_alpha = {}
                tmp_alpha_l = []
                random_order = list(range(0,26))
                random.shuffle(random_order)
            
                for z in random_order:
                    a = chr(z+97)
                    #print( '-------'+a+'--------' )
                    #print( brute_chi_dict[a] )
                    for k,v in brute_chi_dict[a].items():
                        if k not in used_list:
                            used_list.append(k)
                            tmp_alpha[ord(k)-97] = z  #ord(a)-97    #[a]->b or [b]->a?
                            break
                for x in range(0,26):
                    tmp_alpha_l.append( tmp_alpha[x] )

                print( tmp_alpha )
                print( tmp_alpha_l )
                c += 1
        else: 
            #placeholder
            use_case = 3 
    else: #no freq_analysis 
        if respect_spaces and word_guess: 
            for word in unique_len_matches[len(word_guess)][1]: 
                alpha = [ '~' for _ in range(26) ]
                alpha_1 = list(range(0,26))
                exclude_list = []
                exclude_pos = []
                print('------'+word_guess+'=>'+word+'--------')
                for i, lett in enumerate(word):
                    #print( str(i)+'  '+lett )
                    #set guess word in alphabet
                    alpha[ord(lett)-97] = ord(word_guess[i])-97
                    alpha_1.remove(ord(word_guess[i])-97)
                    #exclude_list.append(ord(word_guess[i])-97)
                    exclude_pos.append(ord(lett)-97)
                #print('alpha')
                #print(alpha)
                random.shuffle(alpha_1)
                #print('alpha_1')
                #print(alpha_1)
                c = 0
                for i in range(0,26):
                    if i not in exclude_pos:
                        alpha[i] = alpha_1[c]
                        c += 1
                #print('alpha')
                print(alpha)
                plaintext = decrypt( ciphertext, alpha )
                print( plaintext )


                #populate rest of alphabet randomly
        elif respect_spaces:
            c = 1
            while c <= 100:
                alpha_copy = list(range(0,26))
                random.shuffle(alpha_copy) 
                print( alpha_copy )
                plaintext = decrypt( ciphertext, alpha_copy )
                print( plaintext )
                c += 1
        else: 
            c = 1
            while c <= 100:
                alpha_copy = list(range(0,26))
                random.shuffle(alpha_copy) 
                print( alpha_copy )
                plaintext = decrypt( ciphertext, alpha_copy )
                print( plaintext )
                c += 1



    plaintext = ''


