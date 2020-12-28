from main import *

class Token:
    def __init__(self, s):
        self.s = s
        # self = self.parse()
    def __repr__(self):
        return self.s
    def parse(self):
        s = self.s.strip()

        simpleOperators = [
            ('+', Sum),
            ('-', Subtract),
            ('*', Multiplication),
            ('^', Power),
        ]

        if s.startswith('(') and s.endswith(')'):
            return Token(s[1:-1]).parse()

        if '(' in s:
            count = 0 #TODO
            for i, c in enumerate(s, 1):
                if c == '(': count += 1
                if c == ')': count -= 1
                if count == 0: break
            # print("#", s[:i], s[i:])
            # print("#op", s[i])
            token1 = Token(s[:i]).parse()
            token2 = Token(s[(i+1):]).parse()
            # print('#token1', token1)
            # print('#token2', token2)
            for symbol, operator in simpleOperators:
                if symbol in s[i]:
                    return operator(token1, token2)
            return None #TODO


        for symbol, operator in simpleOperators:
            if symbol in s:
                tokens = s.split(symbol, 1)
                return operator(Token(tokens[0]).parse(), Token(tokens[1]).parse())

        try:
            if int(s) or False:
                return Number(int(s))
        except ValueError:
            pass

        if len(s) == 1 and s.isalpha():
            return Variable(s)

        print("No match!", s)

tests = [
#OK:
    Token('1 + 2'),
    Token('(1+2)'),
    Token('1+x'),
    Token('1*2'),
    Token('1*2*3'),
#TODO:
    # Token('(1+2)+3'),
    # Token('(1*2)*3'),
    # Token('(x*2^2)'),
]

for test in tests:
    print(test)
    simplifyAll(test.parse())
    print('–––')
