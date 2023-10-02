import re
import argparse
import json
import sys

def process_args( ):
    parser = argparse.ArgumentParser( prog="dict_search",
                                      description="tries to match text against dictonary words" )
    parser.add_argument( "input_file" )

    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    if file_to_read == '-':
        input_txt = sys.stdin.read()
    else:
        f = open( file_to_read, "r" )
        input_txt = f.read()
    return input_txt


def split_by_length( input_str ):
    dict_by_word_length = {}
    for line in dict_lines:
        line = line.strip()
        if len( line ) not in dict_by_word_length:
            dict_by_word_length[ len( line ) ] = []
        dict_by_word_length[ len( line ) ].append(line)
    return dict_by_word_length

#add version that can add spaces on detected word boundries


def dict_match( input_str, dict_by_word_length ):
    string_mask = ""
    current_position = 0
    non_match_chars = 0
    prev_match_len = 0
    longest_word = max( dict_by_word_length.keys() )
    #print( '   longest word: {}'.format( longest_word ) )
    while current_position < len( input_str ) -1:
        for i in range( longest_word, 0, -1 ): 
            if i in dict_by_word_length:
                #print( i )
                test_word = input_str[ slice(current_position, current_position+i ) ].lower()
                #print( '    trying test word: "{}"'.format( test_word ) )
                if test_word in dict_by_word_length[i]:
                    #print( 'FOUND WORD {}'.format( test_word ) )
                    string_mask += "X" * i
                    current_position += i
                    prev_match_len = i
                    break
            if i == 1:
                #print( 'have tried entire dict, skipping this char "{}"'.format( input_str[current_position] ) )
                if input_str[current_position] not in " 1234567890.,?!":
                    non_match_chars += 1 + prev_match_len
                    prev_match_len = 0
                    string_mask += ' '
                else:
                    if input_str[current_position] == ' ':
                        string_mask += '_'
                    else:
                        string_mask += input_str[current_position]
                current_position += 1
    return json.dumps( {'mask':string_mask, 'non_match_chars':non_match_chars } )


#  simple words missing from wlist_match12.txt  a  to so
#  I've manually added these
if __name__ == "__main__":
    args = process_args()
    input_txt = load_file( args.input_file )
    input_txt = input_txt.replace("\n", "" )
    dict_file = open( "/home/nvolenec/crypt_tools/wlist_match12.txt", "r" )
    dict_lines = dict_file.readlines()
    dict_by_word_length = split_by_length( dict_lines )
    dict_match_ret = json.loads( dict_match( input_txt, dict_by_word_length ) )

    #print( 'all 1 letter words: {}'.format( dict_by_word_length[1] ) )
    #print( 'all 2 letter words: {}'.format( dict_by_word_length[2] ) )

    offset1 = 0
    offset2 = 60
    leng = len(input_txt)
    while offset1 < leng:
        print( input_txt[   slice( offset1, offset2 ) ] )
        print( dict_match_ret['mask'][ slice( offset1, offset2 ) ] )
        offset1 = offset2
        offset2 += 60
    print( '\n {} matches of {} chars, {:.1%}'.format( leng-dict_match_ret['non_match_chars'], 
                                                      leng, 
                                                      (leng-dict_match_ret['non_match_chars'])/leng ) )

