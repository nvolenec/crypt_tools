import argparse
from math import log10

ngram_files = {2:'english_bigrams.txt',
               3:'english_trigrams.txt',
               4:'english_quadgrams.txt',
               5:'english_quintgrams.txt'}

def process_args():
    parser = argparse.ArgumentParser( prog='get_ngrams',
                                      description='get english language ngram frequency data' )
    parser.add_argument( '-l', '--length' )
    args = parser.parse_args()
    return args

#def get_words_of_len( words, wlen ):
#    words_len = [ x for x in words if len(x) == wlen]
#    return words_len

def get_ngram_data( ngram_length ):
    file = ngram_files[ngram_length]
    with open( file, 'r' ) as f:
        ngram_dict = { key.strip(): int(value.strip()) for key, value in (line.split() for line in f) }
    total = ngram_dict.pop('TOTAL')
    return (ngram_dict, total)

def get_ngram_score( ngram_dict, ngram_tot_count, ciphertext ):
    ngram_dict2 = {}
    c = 0
    ngram_len = 0
    for ngram, n in ngram_dict2.items():
        if c == 0:
            ngram_len = len(ngram)
            c += 1
        ngram_dict2[ngram] = log10(float(n/ngram_tot_count))
    floor = log10(0.01/ngram_tot_count)

    score = 0
    for i in range(len(ciphertext)-ngram_len+1):
        curr_test = ciphertext[i:i+ngram_len]
        if curr_test in ngram_dict:
            score += ngram-dict2[curr_test]
        else: score += floor
    return score

if __name__ == "__main__":
            
    args = process_args()
    if args.length is not None:
        (ngram_dict, total) = get_ngram_data( int(args.length) )

        print( ngram_dict )
        print( 'total: ' + str(total) )


        



