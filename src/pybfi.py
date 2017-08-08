#!/bin/python3

def run_file(filetoread, verbose=False):
    import brainfuck
    try:
        with open(filetoread) as f:
            prog = f.read()
    except Exception as e:
        print("Can't open '{}':{}".format(filetoread, e))
        exit(-1)
    interpreter = brainfuck.Interpreter(verbose=verbose)
    interpreter.interpret_all(prog)

def run_interactive(verbose=None):
 import brainfuck
 interpreter = brainfuck.Interpreter(verbose=verbose)
 print("""PyBFI, a python backed brainfuck interpreter.
Welcome to the interactive interpreter and debugger!
WARNING: The interactive interpreter is still in devloppement and lacks several functionnalities, it may be buggy.""")
 while True:
  interpreter.running = True
  try:
   command = input('》')
   if command == 'exit':
    exit(1)
   else:
    interpreter.interpret_all(command)
    if '.' not in command:
     print(interpreter.memory.read())
    else:
     print()
  except EOFError:
   print("exit")
   exit(0)
  except KeyboardInterrupt:
   print(interpreter.memory.read())
  except Exception as e:
   print("Internal Exception {}".format(e))

if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Brainfuck interpreter.')
    parser.add_argument('file', metavar='file', type=str, nargs='?',
                    help='A script to run.',
                    default=None)
    parser.add_argument('-v', metavar='verbose',
                    help="Allow verbose output (it'really verbose!)",
                    action='store_const', const=True)
    args=parser.parse_args()
    if args.file != None:
     run_file(args.file, verbose=args.v)
    else:
     run_interactive(verbose=args.v)
