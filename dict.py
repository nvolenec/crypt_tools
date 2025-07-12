

class Dict:
    
    def __init__(self, dictfile='google_and_lewis_carroll_dict.txt-sorted', split_by_first_let=0 ):
        with open( dictfile, 'r' ) as f:
            self.words = f.read().splitlines()
        if split_by_first_let:
            self.word_dict = { 'a':[], 'b':[], 'c':[], 'd':[], 'e':[], 'f':[], 'g':[], 'h':[], 'i':[],
                              'j':[], 'k':[], 'l':[], 'm':[], 'n':[], 'o':[], 'p':[], 'q':[], 'r':[],
                              's':[], 't':[], 'u':[], 'v':[], 'w':[], 'x':[], 'y':[], 'z':[] }
            for word in self.words:
                self.word_dict[word[0]].append( word )


    def get_dict(self):
        return self.words

    def get_words_of_len( self, wlen ):
        words_slice = [ x for x in self.words if len(x) == wlen ]
        return words_slice

    def get_words_of_len_starting_with( self, wlen, starting_char ):
        if self.word_dict:
            words_slice = [ x for x in self.word_dict[starting_char] if len(x) == wlen]
        else:
            words_slice = [ x for x in self.words if len(x) == wlen and x[0] == starting_char ]
        return words_slice

    def match_vs_dict_respect_spaces( self, text ):
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
        text_split = text_copy.split()
        while x < text_len:
            for text_word in text_split:
                text_word_len = len( text_word )
                for try_word in self.get_words_of_len_starting_with( text_word_len, text_word[0] ):
                    if try_word == text_word:
                        match_text += try_word
                        x += text_word_len
                        match = 1
                        break
                if match:
                    match = 0
                else:
                    match_text += '~'*text_word_len
                    x += text_word_len
                x += 1
                match_text += '~'  #for spaces between words
        return match_text
    
    def match_vs_dict_ignore_spaces( self, text ):
        #(words, word_dict ) = load_dict()
        text = text.lower()
        text_len = len( text )
        match_text = ''
        x=0
        match = 0
        while x < text_len:
            if text[x] in self.word_dict:
                c_word_list = self.word_dict[text[x]]
                for c_word in c_word_list:
                    c_word_len = len(c_word)
                    if c_word == text[x:x+c_word_len]:
                        match = 1
                        x += c_word_len
                        match_text += c_word
                        break
                if match == 0:
                    match_text += '~'
                    x += 1
                else:
                    match = 0
            else:    #for a character not in word_dict
                x += 1
                match_text += '~'
        return match_text

    def match_vs_dict( self, text, respect_spaces ):
        if respect_spaces:
            return self.match_vs_dict_respect_spaces( text )
        else:
            return self.match_vs_dict_ignore_spaces( text )
