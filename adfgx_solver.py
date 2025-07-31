import argparse
import itertools
import adfgx_tools
import calc_ioc

def process_args():
    parser = argparse.ArgumentParser( prog='adfgx_solver',
                                      description='tries different column transpositions and the resulting ioc to guess transposition then brute forces the polybius square of the most likely candidates' )
    parser.add_argument( 'ciphertext_file' )
    parser.add_argument( '-l', '--transposition_length' )

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = process_args()
    with open( args.ciphertext_file, 'r' ) as f:
        ciphertext = f.read().upper()
    ciphertext = ''.join( filter( str.isalpha, ciphertext ) )
    print( ciphertext )
    print( 'IOC' )
    print( calc_ioc.index_of_coincidence_for_len( ciphertext, 2 ) )

    col_len = 6
    if args.transposition_length:
        col_len = int( args.transposition_length )
    as_word = ''.join( chr(i) for i in range(ord('a'), ord('a')+col_len ) )
    perms = list( itertools.permutations( as_word ) ) 
    trans_ioc = {}
    for perm in perms:
        word = ''.join(perm)
        #print( word )

        col_trans = adfgx_tools.ColTrans(word).decrypt(ciphertext)
        ioc = calc_ioc.index_of_coincidence_for_len( col_trans, 2 )
        trans_ioc[word] = ioc

    #print( trans_ioc )
    for k,v in trans_ioc.items():
        print( '{}: {}'.format(k,v) )


    sorted_trans_ioc = dict( sorted( trans_ioc.items(), key=lambda item: item[1]))

    #key, val = min( sorted_trans_ioc.items(), key=lambda k,v: abs(v-1.0) )
    trans_ioc_swap ={}
    closest_ioc = 0.0667
    closest_word = ''
    for k,v in sorted_trans_ioc.items():
        #build dict of [rounded IOC]: [list of words]
        str_ioc = '{:.3f}'.format(v)
        if str_ioc in trans_ioc_swap:
            trans_ioc_swap[str_ioc].append(k)
        else:
            trans_ioc_swap[str_ioc] = [k]
        #find closest word to an IOC of 1.0
        if abs(0.0667-v) < closest_ioc:
            closest_word = k
            closest_ioc = abs(0.0667-v)
            #print( '{} {}'.format(closest_word, closest_ioc) )

    #print( trans_ioc_swap )

    print( 'closest to 0.0667 is {}: {}'.format( closest_word, closest_ioc ) )
    print( trans_ioc[closest_word] )
    print( adfgx_tools.ColTrans(word).decrypt(ciphertext) )

    #map pairs to single letters
    mapping1 = { 'A': 0, 'D': 5, 'F':10, 'G':15, 'X':20 }
    mapping2 = { 'A': 0, 'D': 1, 'F':2, 'G':3, 'X':4 }
    mapped_ciphertext = ''
    for i in range(0, len(ciphertext), 2):
        mapped_ciphertext += chr(mapping1[ciphertext[i]]+mapping2[ciphertext[i+1]]+ord('A'))
    print( 'mapped ciphertext' )
    print( mapped_ciphertext )
    print( 'mapped_ciphertext IOC' )
    print( calc_ioc.index_of_coincidence( mapped_ciphertext ) )

    to_test_words = []
    if '0.0667' in trans_ioc_swap:
        to_test_words.append( trans_ioc_swap['1.000'] )
    for i in range(1,100):
        if len( to_test_words ) > 1000:
            break

        str_ioc = '{:.3f}'.format(0.0667-0.001*i)
        if str_ioc in trans_ioc_swap:
            to_test_words.append( trans_ioc_swap[str_ioc] )

        str_ioc = '{:.3f}'.format(0.0667+0.001*i)
        if str_ioc in trans_ioc_swap:
            to_test_words.append( trans_ioc_swap[str_ioc] )


     #print( to_test_words )



