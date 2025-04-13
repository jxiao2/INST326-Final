import argparse
import sys

def main(args):
    pass

def parse_args(arglist):
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", help="Name of player 1")
    parser.add_argument("player2", help="Name of player 2")
    return parser.parse_args(arglist)
    
    
    

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)