import argparse
import get_from_dict


def parse_args():
    parser = argparse.ArgumentParser( prog='match_vs_dict',
                                      description='tries to match a text against words in the dictionary' )
    parser.add_argument( '-t', '--text' )
    parser.add_argument( '-f', '--textfile' )
    args = parser.parse_args()
    return args

def load_dict():
    with open( 'google_and_lewis_carroll_dict.txt-sorted', 'r' ) as f:
        words = f.read().splitlines()
    word_dict = { 'a':[], 'b':[], 'c':[], 'd':[], 'e':[], 'f':[], 'g':[], 'h':[], 'i':[],
                  'j':[], 'k':[], 'l':[], 'm':[], 'n':[], 'o':[], 'p':[], 'q':[], 'r':[],
                  's':[], 't':[], 'u':[], 'v':[], 'w':[], 'x':[], 'y':[], 'z':[] }
    for word in words:
        word_dict[word[0]].append( word )

    return( words, word_dict )

def match_vs_dict( text, respect_spaces ):
    if respect_spaces:
        return match_vs_dict_respect_spaces( text )
    else:
        return match_vs_dict_ignore_spaces( text )

def match_vs_dict_respect_spaces( text ):
    (words, word_dict ) = load_dict()
    text = text.lower()
    text_len = len( text )
    match_text = ''
    x=0
    match = 0
    text_copy = text
    text_copy = text_copy.replace(',', ' ')
    text_copy = text_copy.replace('.', ' ')
    text_copy = text_copy.replace(':', ' ')
    text_copy = text_copy.replace(':', ' ')
    text_copy = text_copy.replace('\'', ' ')
    #print( text_copy )
    text_split = text_copy.split()
    while x < text_len:
        for text_word in text_split:
            text_word_len = len( text_word )
            for try_word in get_from_dict.get_words_of_len_starting_with( text_word_len, text_word[0] ):
                if try_word == text_word:
                    match_text += try_word
                    x += text_word_len
                    match = 1
                    break
            if match:
                match = 0
            else:
                match_text += '~'*text_word_len
                x += text_word_len
            x += 1
            match_text += '~'  #for spaces between words
    return match_text

def match_vs_dict_ignore_spaces( text ):
    (words, word_dict ) = load_dict()
    text = text.lower()
    text_len = len( text )
    match_text = ''
    x=0
    match = 0
    while x < text_len:
        if text[x] in word_dict:
            c_word_list = word_dict[text[x]]
            for c_word in c_word_list:
                c_word_len = len(c_word)
                if c_word == text[x:x+c_word_len]:
                    match = 1
                    x += c_word_len
                    match_text += c_word
                    break
            if match == 0:
                match_text += '~'
                x += 1
            else:
                match = 0
        else:    #for a character not in word_dict
            x += 1
            match_text += '~'
    return match_text


if __name__ == "__main__":
    args = parse_args()
    (words, word_dict ) = load_dict()
    text = ''
    if args.text is not None:
        text = args.text
    if args.textfile is not None:
        f = open(args.textfile, 'r')
        text = f.read()
        f.close()
    #match_text = match_vs_dict(text, 0)
    match_text = match_vs_dict(text, 1)
    print( text )
    print( match_text )
    no_match_count = match_text.count('~')
    print( 'matched '+str(len(text)-no_match_count)+' of '+str(len(text))+' characters, match '+str(((len(text)-no_match_count)/len(text))*100)+'%' )
    #improve this calc by subtracting spaces from count







