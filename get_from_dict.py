import argparse

def process_args():
    parser = argparse.ArgumentParser( prog='get_from_dict',
                                      description='get whole or parts of dict file' )
    parser.add_argument( '-l', '--length' )
    args = parser.parse_args()
    return args

def get_dict_file():
    with open( 'google_and_lewis_carroll_dict.txt-sorted', 'r' ) as f:
        words = f.read().splitlines()
    return words


def get_words_of_len( wlen ):
    words = get_dict_file()
    words_slice = [ x for x in words if len(x) == wlen]
    return words_slice

def get_words_of_len_starting_with( wlen, starting_char ):
    words = get_dict_file()
    words_slice = [ x for x in words if len(x) == wlen and x[0] == starting_char ]
    return words_slice


if __name__ == "__main__":
    args = process_args()
    #with open( 'google_and_lewis_carroll_dict.txt-sorted', 'r' ) as f:
    #    words = f.read().splitlines()
    if args.length is not None:
        print( get_words_of_len( int(args.length) ) )



