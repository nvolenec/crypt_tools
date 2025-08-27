import argparse
from math import log10
from get_ngrams import get_ngram_data

def process_args():
    parser = argparse.ArgumentParser( prog='ngram_score',
                                      description='generate ngram score based on specified text and ngram length',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog="e.x. for trigrams: hellotherefriend -> -42.624902\n"
                                             "                   zuaayfzuruoriueb -> -75.711233\n"
                                             "                   ejzzfgejljmlsjwk -> -90.312349\n"
                                             "                   ghnnctghshisuhoe -> -64.815609\n"
                                             "                   ikggrzikykfyqkld -> -91.449079\n"
                                             "                   akhhuqakfktfjkdo -> -89.589869\n"
                                             "                   gayynvgarahrpadl -> -68.828649\n"
                                             "                   pottgipoaovakosb -> -68.253187\n"
                                             "                   hozznjhowolwuobx -> -81.541286\n")
    parser.add_argument( '-l', '--length' )
    parser.add_argument( '-c', '--ciphertext' )
    parser.add_argument( '-f', '--cipherfile' )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = process_args()
    ciphertext = ''
    if args.ciphertext is not None:
        ciphertext = args.ciphertext
    if args.cipherfile is not None:
        f = open(args.cipherfile, 'r')
        ciphertext = f.read()
        f.close()
    if args.length is not None:
        ngram_len = int(args.length)
        if len(ciphertext) > ngram_len:
            (ngram_dict, ngram_tot_count) = get_ngram_data( ngram_len )
            ngram_dict2 = {}
            for ngram, n in ngram_dict.items():
                ngram_dict2[ngram] = log10(float(n/ngram_tot_count))
            floor = log10(0.01/ngram_tot_count)

            score = 0
            for i in range(len(ciphertext)-ngram_len+1):
                curr_test = ciphertext[i:i+ngram_len]
                if curr_test in ngram_dict:
                    score += ngram_dict2[curr_test]
                #if ciphertext[i:i+ngram_len] in ngram_dict: score += ngram_dict[ciphertext[i:i+ngram_len]]
                else: score += floor
    print(score)



