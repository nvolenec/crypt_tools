import argparse
import math

def process_args():
    parser = argparse.ArgumentParser( prog='wordsearch_solver', description='will find words in a block of letters')
    parser.add_argument( 'searchbox')
    parser.add_argument( '-w', '--wordlist')
    parser.add_argument( '-r', '--remove_as_found', action='store_true')
    parser.add_argument( '-d', '--directions') #u,d,l,r,ul,ur,dl,dr
                                                            #1,5,3,7,2 ,8 ,6 ,4
    args = parser.parse_args()
    return args

def find_letter(letter, searchbox):
    results = []
    for x in range(len(searchbox)):
        for y in range(len(searchbox[x])):
            if searchbox[x][y] == letter:
                results.append( (x,y) )
    return results

def is_adjacent( loc1, loc2 ):
    x1, y1 = loc1
    x2, y2 = loc2
    direction = ''

    if x1 == x2-1:
        #down
        direction += 'd'
    elif x1 == x2+1:
        #up
        direction += 'u'

    if y1 == y2-1:
        #left
        direction += 'l'
    elif y1 == y2+1:
        #right
        direction += 'r'

    if abs(y1 - y2) > 1 or abs(x1 - x2) > 1:
        direction = ''

    if len( direction ) > 0:
        #print( '({},{}) -> ({},{}) {}'.format( x1, y1, x2, y2, direction) )
        return direction_lett_to_num( direction )
    else:
        return False

def direction_lett_to_num( dir ):
    response = 0
    if dir == 'ur': response = 2
    elif dir == 'ul': response = 8
    elif dir == 'u':  response = 1
    elif dir == 'r':  response = 3
    elif dir == 'dr': response = 4
    elif dir == 'dl': response = 6
    elif dir == 'd':  response = 5
    elif dir == 'l':  response = 7
    return response

def move_in_direction( pos, dir, spaces=1 ):
    if isinstance( dir, str ):
        direction = direction_lett_to_num( dir )
    else:
        direction = dir
    pos0 = pos[0]
    pos1 = pos[1]
    if direction == 1 or direction == 2 or direction == 8:  #up
        pos0 -= spaces
    if direction == 4 or direction == 5 or direction == 6: #down
        pos0 += spaces
    if direction == 2 or direction == 3 or direction == 4: #right
        pos1 += spaces
    if direction == 6 or direction == 7 or direction == 8: #left
        pos1 -= spaces

    if pos0 >= 0 and pos1 >= 0:  #needs bounds checking on other sides of searchspace too
        return (pos0, pos1)
    else:
        return False

def get_all_adjacent(pos, searchbox):
    adj = []
    pos0 = pos[0]
    pos1 = pos[1]
    adj.append( (pos0-1, pos1) ) #1
    adj.append( (pos0-1, pos1+1) ) #2
    adj.append( (pos0,   pos1+1) ) #3
    adj.append( (pos0+1, pos1+1) ) #4
    adj.append( (pos0+1, pos1) ) #5
    adj.append( (pos0+1, pos1-1) ) #6
    adj.append( (pos0,   pos1-1) ) #7
    adj.append( (pos0-1, pos1-1) ) #8
    return adj

def evaluate_word(word, start_pos, dir, searchbox):
    fail = False
    curr_pos = start_pos
    for a in range(0, len(word)):
        if word[a] != searchbox[curr_pos[0]][curr_pos[1]]:
            fail = True
            break
        curr_pos = move_in_direction( curr_pos, dir )
    if fail:
        return False
    return True

#TODO: right now I'm scanning 29*22 for first 2 letters, maybe it makes more sense to find the least freq. letter
#in the word then work outwards from that so it'll only need to look at 6 per. letter
def find_word_in_block( word, word_letter_map, searchbox ):
    letters_in_word = len(word)
    first = 1
    for x in range( 0, letters_in_word ):
        if first:
            smallest = len(word_letter_map[x])
            smallest_indx = x
            first = 0
        if len(word_letter_map[x]) < smallest:
            smallest = len(word_letter_map[x])
            smallest_indx = x

    curr_indx = smallest_indx
    for pos in word_letter_map[curr_indx]:
        adj_list = get_all_adjacent( pos, searchbox )
        dir = 1
        for adj in adj_list:
            adj_oor = opp_adj_oor = False
            if adj[0] >= len(searchbox) or adj[1] >= len(searchbox[0]): #out of range
                adj_oor = True
            opp_dir = 8 if (dir + 4) % 8 == 0 else (dir + 4) % 8
            if adj_list[opp_dir-1][0] >= len(searchbox) or adj_list[opp_dir-1][1] >= len(searchbox[0]): #out of range
                opp_adj_oor = True
            #next letter
            if curr_indx+1 >= len(word) or searchbox[adj[0]][adj[1]] == word[curr_indx+1]:
                #prev letter
                if curr_indx == 0 or searchbox[adj_list[opp_dir-1][0]][adj_list[opp_dir-1][1]] == word[curr_indx-1]:
                    first_lett_pos = move_in_direction( pos, (dir+4)%8, curr_indx ) #get pos of start of word
                    if evaluate_word(word, first_lett_pos, dir, searchbox):
                        return ( first_lett_pos, dir )
            dir += 1
    return False


def print_searchbox(searchbox):
    for x in range(len(searchbox)):
        str = ''
        for y in range(len(searchbox[x])):
            str += searchbox[x][y]+' '
        print( str )



def rotate_searchbox(searchbox, angle):
    rot_searchbox = []
    if angle == 90:
        return list(zip(*searchbox[::-1]))
    if angle == 45:
        for x in range(len(searchbox)+1):
            rot_searchbox.append([])
            for y in range(len(searchbox[0])+1): #assumes searchbox is not irregular
                rot_searchbox[x].append( '.' )

        for a in range( len(searchbox),0 ):
            x = a
            y = 0
            c = 0
            while x > 0 and y > 0 and y < len(searchbox[0]+1): #main axis
                rot_searchbox[math.ceil(len(searchbox[0])/2.0)][c] = searchbox[x][y]
                c += 1
                x -= 1
                y += 1
    return rot_searchbox


# TODO:  keep original array even if remove as found flag is set
# as we find words store as a dict off of wordlist with coord and direction, ex: 5,3u

if __name__ == '__main__':
    args = process_args()
    f = open( args.searchbox, 'r')
    searchbox_rows = f.readlines()
    f.close()
    f = open( args.wordlist, 'r')
    wordlist = [line.strip() for line in f]
    f.close()
    allowed_directions = [1,2,3,4,5,6,7,8]
    if args.directions:
        allowed_directions = []
        directions = args.directions.lower().replace(' ', '')
        d_str_arr = directions.split(',')
        for dir in d_str_arr:
            allowed_directions.append( direction_lett_to_num(dir) )

searchbox = []
c= 0
for line in searchbox_rows:
    tmp = line.replace( '\n', '' )
    searchbox.append( [] )
    for a in tmp:
        searchbox[c].append(a)
    c += 1
#print( searchbox )

word_letter_map = {}
for word in wordlist:
    word_letter_map[word] = []
    for l in word:
        word_letter_map[word].append( find_letter(l, searchbox) )

print( '-'+wordlist[0]+'-' )
print( word_letter_map[wordlist[0]] )

#for word in wordlist:
#    results = find_word_in_block( word_letter_map[word] )
#    if results:
#        print( "{} -> {} {}".format( word, results[0], results[1]))
word = 'alice'
results = find_word_in_block( word, word_letter_map[word], searchbox )
if results:
    print( "{} -> {} {}".format( word, results[0], results[1]))

#box = []
#for a in range(0,5):
#    box.append( [] )
#    output_str = ''
#    print( "\n" )
#    for b in range(0,7):
#        box.append( b + a*7)
#        output_str +=  str(b+a*7)+' '
#    print( output_str )

#print("\n\n")
#print_searchbox( searchbox)
#print ("\n\n")
#print_searchbox( rotate_searchbox(searchbox, 45))
