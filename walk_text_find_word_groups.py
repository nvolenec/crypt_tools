
import argparse

def process_args():
    parser = argparse.ArgumentParser( prog='walk_text_find_word_groups',
                                      description='find 2,3,4 word groups from original text' )
    parser.add_argument( 'text_file' )
    parser.add_argument( '-l', '--group_length' )
    args = parser.parse_args()
    return args




if __name__ == "__main__":
    args = process_args()
    with open( args.text_file, 'r' ) as f:
        text = f.read() 
    length = int( args.group_length )

    all_word_groups = {}
    counter = 0
    words = text.split()
    for i in range(0, len(words) ):
        group = words[i:i+length]
        s = ''.join(group)
        if s in all_word_groups:
            all_word_groups[s] += 1
        else:
            all_word_groups[s] = 1
        counter += 1

    print( 'total word groups of size '+str(length)+': '+str(counter) )
    print( 'total unique word groups of size '+str(length)+': '+str(len(all_word_groups)) )

    for k,v in all_word_groups.items():
        print( k )


