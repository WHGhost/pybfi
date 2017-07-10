#!/bin/python3

def main(filetoread, verbose=False):
    import brainfuck
    prog = ''
    try:
        with open(filetoread) as f:
            prog = f.read()
            f.close()
    except Exception as e:
        print("Can't open '{}':{}".format(filetoread, e))
    interpreter = brainfuck.Interpreter(verbose=verbose)
    interpreter.interpret_all(prog)

if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Brainfuck interpreter.')
    parser.add_argument('file', metavar='file', type=str, nargs=1,
                    help='A script to run.')
    parser.add_argument('-v', metavar='verbose',
                    help="Allow verbose output (it'really verbose!)",
                    action='store_const', const=True)
    args=parser.parse_args()
    main(args.file[0], verbose=args.v)
