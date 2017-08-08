import sys


class Interpreter:

    def __init__(self,
            stdin=sys.stdin,
            stdout=sys.stdout,
            verbose=False):
        self.stdin = stdin
        self.stdout = stdout
        self.verbose = verbose
        self.verb("Verbose mode is one.")
        self.verb("Initilized stdin and stdout.")
        self.memory = Memory()
        self.verb("Initialized memory.")
        self.verb("Memory:")
        self.verb(str(self.memory))
        self.loop_depth = 0
        self.verb("Initialized looping depth counter.")
        self.running = True
        self.verb("Running.")
        self.verb("")

    def verb(self, message):
        if self.verbose:
            self.out("[*]" + message + "\n")

    def out(self, string):
        if self.stdout != None:
            self.stdout.write(string)
            self.stdout.flush()

    def read_stdin(self):
        l = self.stdin.read(1)
        if l != '':
            return ord(l)
        return 0

    def interpret_char(self, char):
        if not self.running:
            return
        if char == '<':
            self.verb("Action: move left")
            self.memory.move_left()
            self.verb("Moved left")
            self.verb("Memory:")
            self.verb(str(self.memory))
            self.verb("")
        elif char == '>':
            self.verb("Action: move right")
            self.memory.move_right()
            self.verb("Moved right")
            self.verb("Memory:")
            self.verb(str(self.memory))
            self.verb("")
        elif char == '+':
            self.verb("Action: add")
            self.memory.add()
            self.verb("Added")
            self.verb("Memory:")
            self.verb(str(self.memory))
            self.verb("")
        elif char == '-':
            self.verb("Action: sub")
            self.memory.sub()
            self.verb("Substracted")
            self.verb("Memory:")
            self.verb(str(self.memory))
            self.verb("")
        elif char == ".":
            self.verb("Action: show")
            self.out(chr(self.memory.read()))
        elif char == ",":
            self.verb("Action: show")
            self.memory.write(self.read_stdin())

    def loop(self, code, line):
        if not self.running:
            return
        self.loop_depth += 1
        self.verb("Looping: {}".format(code))
        self.verb("Looping depth is {}.".format(self.loop_depth))
        while self.memory.read() != 0:
            self.interpret_all(code, line=line, raiseExc=True)
        self.verb("Exited a loop.")
        self.verb("Looping depth is {}.".format(self.loop_depth))
        self.loop_depth -= 1

    def interpret_all(self, code, line=1, raiseExc=False):
        if not self.running:
            return
        x = 0
        while x < len(code):
            char = code[x]
            if char == '\n':
                line += 1
            try:
                if char == '[':
                    openned = 1
                    i = x
                    loopline = line
                    while openned > 0 and i < len(code) - 1:
                        i += 1
                        if code[i] == '\n':
                            loopline += 1
                        if code[i] == '[':
                            openned += 1
                        elif code[i] == ']':
                            openned -= 1
                    if openned > 0:
                        self.out("Error: Excepted ']' on line {}\n".format(loopline))
                        self.running = False
                    else:
                        self.loop(code[x+1: i], line=line)

                        x = i + 1
                        continue

                self.interpret_char(char)
                x += 1
            except Exception as e:
                if not raiseExc:
                    self.running = False
                    self.out("Error on line {}\n".format(line))
                    self.out(str(e) + "\n")
                else:
                    raise e
            except KeyboardInterrupt as e:
                if not raiseExc:
                    self.running = False
                    self.out("\nKeyboard interrupt on line {}\n".format(line))
                else:
                    raise e

class Memory:

    def __init__(self):
        self.mem=[0,]
        self.pointer=0
        self.delta=0

    def read(self):
        return self.mem[self.pointer + self.delta]

    def write(self, val):
        self.mem[self.pointer + self.delta] = val

    def move_right(self):
        if len(self.mem) <= self.pointer + self.delta + 1:
            self.mem.append(0)
        self.pointer += 1

    def move_left(self):
        if 0 > self.pointer + self.delta - 1:
            self.mem.insert(0, 0)
            self.delta += 1
        self.pointer -= 1

    def add(self):
        self.mem[self.pointer + self.delta] += 1

    def sub(self):
        self.mem[self.pointer + self.delta] -= 1

    def __str__(self):
        return str(self.mem) + "p={};d={}".format(self.pointer, self.delta)
