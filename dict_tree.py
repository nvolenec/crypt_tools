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

    def match_vs_dict_single_word( self, text ):
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


    def match_vs_dict( self, guess_plaintext ):
        txt_len = len( guess_plaintext )
        x = 0
        match_text = ''
        while x < txt_len:
            longest_word = self.match_vs_dict_single_word( guess_plaintext[x:x+16] )
            if len(longest_word) > 0:
                x += len(longest_word)
                match_text += longest_word
            else:
                match_text += '~'
                x += 1
        
        return match_text


    def match_vs_dict_respect_spaces( self, guess_plaintext ):
        txt_len = len( guess_plaintext )
        x = 0
        match_text = ''
        words = guess_plaintext.split(' ')
        for word in words:
            longest_word = self.match_vs_dict_single_word( word )
            if len(longest_word) == len(word):
                match_text += longest_word
            else:
                match_text += '~'*len(longest_word)
            x += len(longest_word)
        
        return match_text
    

