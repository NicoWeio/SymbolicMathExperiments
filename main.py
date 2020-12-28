class Number:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)
    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
    def simplify(self):
        return self
    def deriv(self, by):
        return Number(0)

class Variable:
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name
    def __repr__(self):
        return str(self.name)
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == othe
    def simplify(self):
        return self
    def deriv(self, by):
        if self == by:
            return Number(1)
        else:
            return Number(0)

class Sum:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} + {self.right})"
    def __eq__(self, other):
        if isinstance(other, Sum):
            return (self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)
        else:
            return False #TODO!
    def simplify(self):
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(self.left.value + self.right.value)
        if self.left == self.right:
            return Multiplication(Number(2), self.left)
        if self.left == 0:
            return self.right
        if self.right == 0:
            return self.left
        return Sum(self.left.simplify(), self.right.simplify())
    def deriv(self, by):
        return Sum(self.left.deriv(by), self.right.deriv(by))

class Subtract:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} - {self.right})"
    def __eq__(self, other):
        if isinstance(other, Subtract):
            return (self.left == other.left and self.right == other.right)
        else:
            return False #TODO!
    def simplify(self):
        if self.left == self.right:
            return Number(0)
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(self.left.value - self.right.value)
        return Subtract(self.left.simplify(), self.right.simplify())
    def deriv(self, by):
        return Subtract(self.left.deriv(by), self.right.deriv(by))

class Multiplication:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} * {self.right})"
    def __eq__(self, other):
        if isinstance(other, Multiplication):
            return (self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)
        else:
            return False #TODO!
    def simplify(self):
        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(self.left.value * self.right.value)
        if self.left == Number(0) or self.right == Number(0):
            return Number(0)
        if self.left == Number(1):
            return self.right
        if self.right == Number(1):
            return self.left
        if self.left == self.right:
            return Power(self.left, Number(2))
        if isinstance(self.left, Number) and isinstance(self.right, Sum):
            return Sum(Multiplication(self.left, self.right.left), Multiplication(self.left, self.right.right))
        #TODO 0*… → 0
        return Multiplication(self.left.simplify(), self.right.simplify())
    def deriv(self, by):
        # u'v+uv'
        return Sum(Multiplication(Derivative(self.left, by), self.right), Multiplication(self.left, Derivative(self.right, by)))

class Power:
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
    def __repr__(self):
        def superscript(num):
            map = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
            return ''.join([map[int(s)] for s in str(num)])
        if isinstance(self.exponent, Number):
            return f"{self.base}{superscript(self.exponent.value)}"
        else:
            return f"({self.base}^{self.exponent})"
    def __eq__(self, other):
        if isinstance(other, Power):
            return self.base == other.base and self.exponent == other.exponent #TODO!
        else:
            return False #TODO!
    def simplify(self):
        # if isinstance(self.base, Power):
        #     return Power(TODO)
        if self.exponent == Number(0):
            if self.base == Number(0):
                raise ValueError("0^0")
            else:
                return Number(1)
        if isinstance(self.base, Number) and isinstance(self.exponent, Number):
            assert self.exponent.value > 0
            return Number(self.base.value ** self.exponent.value)
        if isinstance(self.base, Power):
            return Power(self.base.base, Multiplication(self.base.exponent, self.exponent))
        if self.exponent == Number(1):
            return self.base
        return Power(self.base.simplify(), self.exponent.simplify())
    def deriv(self, by):
        if isinstance(self.exponent, Number):
            return Multiplication(Multiplication(self.exponent, Power(self.base, Subtract(self.exponent, Number(1)))), self.base.deriv(by))
        return None

class Derivative:
    def __init__(self, term, by):
        assert isinstance(by, Variable)
        self.term = term
        self.by = by
    def __repr__(self):
        return f"(d/d{self.by} {self.term})"
    def simplify(self):
        return self.term.deriv(self.by).simplify()

tests = [
# OKAY:
    (Number(2), Number(2)),

    (Sum(Number(2), Number(3)), Number(5)),
    (Sum(Sum(Number(2), Number(3)), Sum(Number(2), Number(3))), Number(10)),
    (Sum(Sum(Variable('x'), Number(3)), Sum(Variable('x'), Number(3))), Sum(Multiplication(Number(2), Variable('x')), Number(6))),

    (Subtract(Number(2), Number(3)), Number(-1)),
    (Subtract(Variable('x'), Variable('x')), Number(0)),
    (Subtract(Sum(Number(2), Number(3)), Sum(Number(2), Number(3))), Number(0)),
    (Subtract(Sum(Variable('x'), Number(3)), Sum(Variable('x'), Number(3))), Number(0)),

    (Multiplication(Sum(Number(2), Number(3)), Number(10)), Number(50)),
    (Multiplication(Number(10), Sum(Number(2), Variable('x'))), Sum(20, Multiplication(Number(10), Variable('x')))),

    (Derivative(Number(2), Variable('x')), Number(0)),
    (Derivative(Variable('x'), Variable('x')), Number(1)),
    (Derivative(Sum(Variable('x'), Variable('y')), Variable('x')), Number(1)),
    (Derivative(Sum(Number(2), Variable('x')), Variable('x')), Number(1)),
    (Derivative(Multiplication(Number(2), Variable('x')), Variable('x')), Number(2)),
    (Derivative(Multiplication(Variable('x'), Variable('x')), Variable('x')), Multiplication(Number(2), Variable('x'))),

    (Power(Number(10), Number(2)), Number(100)),
    (Power(Number(10), Number(0)), Number(1)),
    (Power(Power(Number(10), Number(2)), Number(2)), Number(10000)),
    (Power(Power(Variable('x'), Number(2)), Number(2)), Power(Variable('x'), Number(4))),
    (Derivative(Power(Number(10), Number(2)), Variable('x')), Number(0)),
    (Derivative(Power(Variable('x'), Number(2)), Variable('x')), Multiplication(Number(2), Variable('x'))),

    (Multiplication(Power(Variable('x'), Number(2)), Power(Variable('x'), Number(2))), Power(Variable('x'), Number(4))),
    (Derivative(Multiplication(Variable('x'), Variable('y')), Variable('x')), Variable('y')),
    (Multiplication(Sum(Variable('x'), Variable('y')), Sum(Variable('y'), Variable('x'))), Power(Sum(Variable('x'), Variable('y')), Number(2))),
    (Sum(Multiplication(Variable('x'), Variable('y')), Multiplication(Variable('y'), Variable('x'))), Multiplication(Number(2), Multiplication(Variable('x'), Variable('y')))),
# TODO:
    # (Subtract(Number(0), Variable('x')), Multiplication(Number(-1), Variable('x'))),
    # Power(Number(0), Number(0)),
]

def simplifyAll(term):
    prev = None
    val = term
    iters = 0
    # while (str(val) != str(prev)):
    while (val != prev):
        prev = val
        iters += 1
        val = val.simplify()
        if prev != val:
            print(val)
        if iters > 5:
            print("NOPE")
            break
    return val

def doTests():
    for test, result in tests:
        print(f"→ {test} # SOLL: {result}")
        prev = None
        val = test
        iters = 0
        # while (str(val) != str(prev)):
        while (val != prev):
            prev = val
            iters += 1
            val = val.simplify()
            if prev != val:
                print(val)
            if iters > 5:
                print("NOPE")
                break
        if (val != result):
            print("FALSCH!")
        print('–––')

doTests()
