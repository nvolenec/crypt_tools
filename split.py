import re
import argparse


def process_args( ):
    parser = argparse.ArgumentParser( prog="split",
                                      description="Split a file into multiple files based on the string 'PAGE'" )
    parser.add_argument( "input_file" )
    args = parser.parse_args()
    return args


def load_file( file_to_read ):
    f = open( file_to_read, "r" )
    return f


def do_split( input_str ):
    return re.split( r"(PAGE \d+)", input_str )


if __name__ == "__main__":
    args = process_args()
    input_file = load_file( args.input_file )
    input_txt = input_file.read()
    input_split = do_split( input_txt )
    counter = 1
    for s1, s2 in zip( input_split[::2], input_split[1::2] ):
        print ( "------{}------".format(counter) )
        counter = counter + 1
        print( s1, s2 )
        file_to_write = s2.replace( ' ', '' )
        with open( file_to_write, "w" ) as f:
            f.write( s1 )
            f.write( s2 )
        


