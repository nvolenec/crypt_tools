import argparse
import calc_ioc


def process_args():
    parser = argparse.ArgumentParser( prog='examine_ciphertext',
                                      description='runs basic stats on ciphertext' )
    parser.add_argument( 'ciphertext_file' )
    args = parser.parse_args()
    return args

def friedman_test( ic, n ):
    # k = ( 0.0265 * N ) / (N -1 ) * IC - 0.0385 * N + 0.065
    return (0.0265 * n)/(((n-1) * ic) - (0.0385 * n) + 0.065)


if __name__ == "__main__":
    args = process_args()
    with open( args.ciphertext_file, 'r' ) as f:
        ciphertext = f.read().lower()

    if ' ' in ciphertext:
        words = ciphertext.split()
        word_dict_count = Counter(words)
        word_len_count = {}
        for word in words:
            if len(word) in word_len_count:
                word_len_count[len(word)] += 1
            else:
                word_len_count[len(word)] = 1
        #if len( word_len_count ) > 1: #checking if ciphertext is fixed blocks or space seperated words


    

    ic = calc_ioc.index_of_coincidence( ciphertext )
    print( 'Index of Coinidence: '+str(ic) )
    friedman = friedman_test( ic, len(ciphertext) )
    print( 'Friedman Test - estimated key lenth: '+str(friedman) )



