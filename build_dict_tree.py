import treelib

def build_tree(words):
    tree = treelib.Tree(identifier='tree')
    tree.create_node( 'root', 'rootROOT' )
    print( '    adding root' )
    for word in words:
        if len(word) == 1:
            tree.create_node( word, word, parent='rootROOT' )
            print( '    adding word '+word+' child of root' )
        else:
            #tree.add_node(node, parent='parent')
            #trav = tree['root']
            running_word_prev = ''
            running_word = ''
            for letter in word:
                running_word += letter
                print( running_word+'('+str(len(running_word))+') '+running_word_prev+'('+str(len(running_word_prev))+')' )
                running_node = tree.get_node(running_word)
                running_node_prev = tree.get_node(running_word_prev)
                if running_node is None:
                    if running_word == word:
                        tree.create_node( word, word, parent=running_node_prev.identifier )
                        print( '    adding word '+word+' child of '+running_node_prev.identifier )
                    else:
                        if len(running_word_prev) == 0:
                            tree.create_node( 'NOTAWORD', running_word, parent='rootROOT' )
                            print( '    adding node '+running_word+'NOTAWORD child of '+'rootROOT'  )
                        else:
                            tree.create_node( 'NOTAWORD', running_word, parent=running_node_prev.identifier )
                            print( '    adding node '+running_word+'NOTAWORD child of '+running_node_prev.identifier )
                running_word_prev += letter
    return tree


def filter_fn( word ):
    def filter_func( node ):
        #print( '-- ' + word + '   ' + node.identifier )
        if node.identifier == 'rootROOT':
            return True
        return word.startswith(node.identifier)
    return filter_func

def print_filter(node):
    print(node.identifier)
    return True


if __name__ == "__main__":

    with open( 'google_and_lewis_carroll_dict.txt-short-long', 'r' ) as f:
        words = [lines.rstrip('\n') for lines in f]

    tree= build_tree(words)

    print( 'total nodes: '+str(tree.size()) )
    print( 'max depth: '+str(tree.depth()) )

    #tree.show()

    words = ['disrespectful', 'andthesunrises', 'applesintherain', 'disrespect']
    n = None
    for word in words:
        print( '-------------------------' )
        nodes_g = tree.expand_tree(nid='rootROOT', mode=treelib.Tree.DEPTH, filter=filter_fn(word))
        #nodes_g = tree.expand_tree(nid='a', mode=treelib.Tree.DEPTH, filter=f1)

        for n in nodes_g:
            a = tree.get_node(n)
            if a.tag != 'NOTAWORD' and a.identifier != 'rootROOT':
                print(a.identifier)

        nodes_g = tree.expand_tree(nid='rootROOT', mode=treelib.Tree.WIDTH, filter=filter_fn(word))
        #nodes_g = tree.expand_tree(nid='a', mode=treelib.Tree.DEPTH, filter=f1)

        for n in nodes_g:
            a = tree.get_node(n)
            if a.tag != 'NOTAWORD' and a.identifier != 'rootROOT':
                print(a.identifier)

    #print( '======================================' )
    #for word in words:
    #    print( '-------------------------' )
    #    nodes_g = tree.expand_tree(nid=word[0], mode=treelib.Tree.DEPTH, filter=filter_fn(word))

    #    for n in nodes_g:
    #        a = tree.get_node(n)
    #        print(a.tag)

    #print( '======================================' )
    #for word in words:
    #    print( '-------------------------' )
    #    nodes_g = tree.expand_tree()

    #    for n in nodes_g:
    #        a = tree.get_node(n)
    #        print(a.tag)

    #print( '======================================' )
    #for word in words:
    #    print( '-------------------------' )
    #    nodes_g = tree.expand_tree(filter=print_filter)

    #    for n in nodes_g:
    #        a = tree.get_node(n)
    #        print(a.tag)

        #while len(word) > 0:
        #    if n is None:
        #        n = tree.get_node( word )
        #        print( 'get_node('+word+')' )
        #    else:
        #        #pre_id = n.predecessor('tree')  #not predecessor returns a string
        #        #n = tree.parent( prev_word )
        #        tree.get_node( pre_id )
        #        #print( 'get predecessor() = '+n.identifier )
        #    if n is None:
        #        print( word+'  not in tree' )
        #    else:
        #        print(word)
        #        print( n.tag+'   '+n.identifier )
        #    print( 'predecessors: ' )
        #    print( n.predecessor('tree') )
        #    print( 'successors: ' )
        #    print( n.successors('tree') )
        #    prev_word = word
        #    word = word[:-1]

