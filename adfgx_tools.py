
# polybiussquare, coltrans, adfgx, and adfgvx based on as https://github.com/jameslyons/pycipher
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class PolybiusSquare:

    def __init__( self, key='phqgiumeaylnofdxkrcvstzwb', size=5, chars=None ):
        self.key = ''.join([k.upper() for k in key])
        self.chars = chars or 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:size]
        self.size = size

    def encrypt_char( self, char ):
        row = (int)(self.key.index(char) / self.size )
        col = self.key.index(char) % self.size
        return self.chars[row] + self.chars[col]

    def decrypt_pair( self, pair ):
        row = self.chars.index(pair[0])
        col = self.chars.index(pair[1])
        return self.key[ row * self.size + col ]

    def encrypt( self, plain ):
        #plain = self.remove_punctuation( plain )
        ret = ''
        for c in range(0,len(plain)):
            ret += self.encrypt_char(plain[c])
        return ret

    def decrypt( self, crypt ):
        #crypt = self.remove_punctuation(crypt)
        ret = ''
        for i in range(0,len(crypt),2):
            ret += self.decrypt_pair(crypt[i:i+2])
        return ret


class ColTrans:
    def __init__( self, keyword='GERMAN' ):
        self.keyword = keyword.upper()
        a = sorted(self.keyword)
        b = range(len(self.keyword))
        c = [(keyword[i],i) for i in range(len(keyword))]
        self.keyword_encrypt_order = []
        for l in self.keyword:
            self.keyword_encrypt_order.append( b[a.index(l)] )
        self.keyword_decrypt_order = [d[1] for d in sorted(c)]
        #print( self.keyword_sorted_ind )
        #print( self.keyword_unsorted_ind )

    def encrypt( self, plaintext ):
        ret = ''
        print( self.keyword_encrypt_order )
        for i in range(len(self.keyword)):
            ret += plaintext[self.keyword_encrypt_order.index(i)::len(self.keyword)]
        return ret


    def decrypt( self, ciphertext ):
        print( self.keyword_decrypt_order )
        ret =  ['_'] * len( ciphertext)
        l = len(ciphertext)
        m = len(self.keyword)
        ind = self.keyword_decrypt_order
        upto = 0
        for i in range(len(self.keyword)):
            thiscollen = int(l/m)
            if ind[i] < l%m: thiscollen += 1
            ret[ind[i]::m] = ciphertext[upto:upto+thiscollen]
            upto += thiscollen
        return ''.join(ret)

class adfgx:
    def __init__(self, key='phqgmeaylnofdxkrcvszwbuti', keyword='GERMAN'):
        self.key = [k.upper() for k in key]
        self.keyword = keyword

    def encrypt( self, plaintext ):
        s1 = PolybiusSquare(self.key, size=5, chars='ADFGX').encrypt(plaintext)
        s2 = ColTrans(self.keyword).encrypt(s1)
        return s2

    def decrypt( self, ciphertext ):
        s2 = ColTrans(self.keyword).decrypt(ciphertext)
        s1 = PolybiusSquare(self.key, size=5, chars='ADFGX').decrypt(s2)
        return s1

class adfgvx:
    def __init__(self, key='phqgmeaylnofdxkrcvszwbuti', keyword='GERMAN'):
        self.key = [k.upper() for k in key]
        self.keyword = keyword

    def encrypt( self, plaintext ):
        s1 = PolybiusSquare(self.key, size=6, chars='ADFGVX').encrypt(plaintext)
        s2 = ColTrans(self.keyword).encrypt(s1)
        return s2

    def decrypt( self, ciphertext ):
        s2 = ColTrans(self.keyword).decrypt(ciphertext)
        s1 = PolybiusSquare(self.key, size=6, chars='ADFGVX').decrypt(s2)
        return s1



if __name__ == '__main__':
    pb = PolybiusSquare(chars='ADFGX')

    print( 'polybius sq encrypt HELLOWORD' )
    cipher = pb.encrypt('HELLOWORLD')
    print( 'ciphertext: {}'.format(cipher) )

    print( 'polybius sq decrypt HELLOWORD' )
    plain = pb.decrypt(cipher)
    print( 'plainext: {}'.format(plain) )

    print( '------------' )
    #######
    print( 'Col Trans GERMAN' )
    ct = ColTrans('GERMAN')
    plaintext = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    print( 'GERMANGERMANGERMANGERMANGERMAN' )
    print( plaintext )
    ciphertext = ct.encrypt(plaintext)
    print( ciphertext )
    pt = ct.decrypt(ciphertext)
    print(pt)
    print( '------------' )

    ad = adfgx('phqgmeaylnofdxkrcvszwbuti','GERMAN')
    ciphertext1 = ad.encrypt(plaintext)
    print(ciphertext1)
    pt1 = ad.decrypt( ciphertext1 )
    print( pt1 )

    print( '------------' )

    adv =adfgvx('phqgmeaylnofdxkrcvszwbuti','GERMAN')
    ciphertext1 = ad.encrypt(plaintext)
    print(ciphertext1)
    pt1 = ad.decrypt( ciphertext1 )
    print( pt1 )

