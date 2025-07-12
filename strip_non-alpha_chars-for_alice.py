import argparse

parser = argparse.ArgumentParser( prog="xxx", description="xxx" )
parser.add_argument( '-i', '--inputfile' )
args = parser.parse_args()

with open( args.inputfile, 'r' ) as f:
    orig = f.read().replace('\n', ' ')

out = ''
for c in orig:
    if c.isalpha():
        out += c
    if c == '--':
        out += ' '
    if c == '-' or c == ' ':
        out += ' '
    #everything else: . , ' " ( ) : ; 

out2 = ' '.join( out.split() )

print( out2 )
