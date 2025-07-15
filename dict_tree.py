import treelib

def filter_fn( word ):
    def filter_func( node ):
        #print( '-- ' + word + '   ' + node.identifier )
        if node.identifier == 'rootROOT':
            return True
        return word.startswith(node.identifier)
    return filter_func

class DictTree:
    
    def __init__(self, dictfile='google_and_lewis_carroll_dict.txt-short-long'):
        with open( dictfile, 'r' ) as f:
            words = f.read().splitlines()
            self.tree = treelib.Tree(identifier='treedict')
            self.tree.create_node( 'root', 'rootROOT' )
            for word in words:
                #self.word_dict[word[0]].append( word )
                if len(word) == 1:
                    self.tree.create_node( word, word, parent='rootROOT' )
                else:
                    running_word = ''
                    running_word_p = ''
                    for letter in word:
                        running_word += letter
                        running_node = self.tree.get_node(running_word)
                        running_node_p = self.tree.get_node(running_word_p)
                        if running_node is None:
                            if running_word == word:
                                self.tree.create_node( word, word, parent=running_node_p.identifier )
                            else:
                                if len( running_word_p ) == 0:
                                    self.tree.create_node( 'NOTAWORD', running_word, parent='rootROOT' )
                                else:
                                    self.tree.create_node( 'NOTAWORD', running_word, parent=running_node_p.identifier )

                        running_word_p += letter


    def get_dicttree(self):
        return self.tree

    def match_vs_dict( self, text ):
        #(words, word_dict ) = load_dict()
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
        #text_split = text_copy.split()
        id_g = self.tree.expand_tree( nid='rootROOT', mode=treelib.Tree.WIDTH, filter=filter_fn(text_copy) )
        matches = []
        for ident in id_g:
            longest_match = ''
            n = self.tree.get_node(ident)
            if n.tag != 'NOTAWORD' and n.identifier != 'rootROOT':
                matches.append( n.identifier )
                #this check is redudant, last match should always be the longest
                if len(n.identifier) > len(longest_match):
                    longest_match = n.identifier

        return longest_match
    

