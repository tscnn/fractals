import sys
import numpy as np
from array import array

MOVE = 0
LINE = 1


class sequence:

    def __init__(self, data=None):
        self.__data = data
        self.__position = 0
    
    def next(self):
        char = self.__data[self.__position]
        return char
    
    def forward(self):
        self.__position += 1
    
    def next_forward(self):
        char = self.next()
        self.forward()
        return char


class number:

    def __init__(self, data):
        if type(data) == float:
            self.__data = data
        else:
            dot = False
            text = ""
            while len(data) > 0:
                c = data[0]
                if c >= '0' and c <= '9':
                    text += data.pop(0)
                elif c == '.' and not dot:
                    dot = True
                    text += data.pop(0)
                else:
                    break
            self.__data = float(text)
    
    def value(self):
        return self.__data
    
    def __str__(self):
        return str(self.__data)


class name:

    def __init__(self, text):
        self.__data = ""
        while len(text) > 0:
            c = text[0]
            if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                self.__data += text.pop(0)
            else:
                break

    def __str__(self):
        return self.__data
        

class operator:
    
    def __init__(self, text):
        self.__data = text.pop(0)
    
    def use(self, number1, number2):
        if self.__data == '*':
            return number(number1.value() * number2.value())
        elif self.__data == '/':
            return number(number1.value() / number2.value())
        elif self.__data == '+':
            return number(number1.value() + number2.value())
        elif self.__data == '-':
            return number(number1.value() - number2.value())
        else:
            raise Exception("operator '%s' not implemented" % self.__data)
    
    def __str__(self):
        return self.__data


class comperator:
    
    def __init__(self, text):
        self.__data = text.pop(0)
    
    def use(self, number1, number2):
        if self.__data == '<':
            return number1.value() < number2.value()
        elif self.__data == '>':
            return number1.value() > number2.value()
        elif self.__data == '=':
            return number1.value() == number2.value()
        else:
            raise Exception("comperator '%s' not implemented" % self.__data)
    
    def __str__(self):
        return self.__data


class expression:
    """ expression := ... """
    
    def __init__(self, text):
        self.__operands = []
        self.__operators = []
        while True:
            if len(text) == 0:
                raise Exception("unexpected end of expr")
            c = text[0]
            if (c >= '0' and c <= '9') or c == '.':
                self.__operands.append(number(text))
            elif (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                self.__operands.append(name(text))
            else:
                raise Exception("%s not allowed in expr" % c)
            if len(text) == 0:
                raise Exception("unexpected end of expr")
            c = text[0]
            if c == ')':
                break
            else:
                self.__operators.append(operator(text))
    
    def evaluate(self, assignment):
        numbers = [o if o.__class__==number else assignment[str(o)] for o in self.__operands]
        result = numbers[0]
        for i in xrange(len(self.__operators)):
            result = self.__operators[i].use(result, numbers[i+1])
        return result
    
    def operands(self):
        return self.__operands
    
    def operators(self):
        return self.__operators
    
    def __str__(self):
        s = str(self.__operands[0])
        for i in xrange(len(self.__operators)):
            s += str(self.__operators[i]) + str(self.__operands[i+1])
        return s


class variable:
    """ variable := variable_name(params) | variable_name
        params := param,params | param
        param := depends on param_class
        variable_name := A | B | ... | Z | a | b | ... | z | + | - (maybe more) """
    
    def __init__(self, data, param_class, assignment=None):
        if type(data) == list:
            self.__name = data.pop(0)
            self.__params = []
            if len(data) > 0 and data[0] == '(':
                data.pop(0)
                while True:
                    self.__params.append(param_class(data))
                    if len(data) == 0:
                        raise Exception("unallowed end of var")
                    c = data[0]
                    if c == ',':
                        data.pop(0)
                    elif c == ')':
                        data.pop(0)
                        break
        elif data.__class__ == variable and param_class == number:
            self.__name = data.name()
            self.__params = []
            for param in data.params():            
                self.__params.append(param.evaluate(assignment))                    
    
    def name(self):
        return self.__name
    
    def params(self):
        return self.__params
    
    def match(self, pattern_variable):
        if self.name() == pattern_variable.name() and len(self.params()) == len(pattern_variable.params()):
            assignment = {}
            for i in xrange(len(self.params())):
                assignment[str(pattern_variable.params()[i])] = self.params()[i]
            return True, assignment
        else:
            return False, None 
    
    def __len__(self):
        return len(self.__params)
    
    def __getitem__(self, key):
        return self.__params[key]
    
    def __str__(self):
        P = self.__params
        if len(P) > 0:
            return "%s(%s)" % (self.name(), ",".join([str(p) for p in P]))
        else:
            return self.name()


class subject:
    """ subject := subject^* | [subject^*] | variable_s """

    def __init__(self, text):
        if type(text) == str:
            text = list(text)
        self.__tokens = []
        while len(text) > 0:
            c = text[0]
            if c == '[' or c == ']':
                self.__tokens.append(text.pop(0))
            elif (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '+' or c == '-':
                self.__tokens.append(variable(text, number))
            else:
                break
     
    def tokens(self):
        return self.__tokens
    
    def __local_pattern_match(self, position, rule):
        pattern = rule.pattern()
        if len(self) - position < len(pattern):
            return False, None
        constraints = rule.constraints()
        assignment = {}
        for i in xrange(len(pattern)):
            st = self[position+i]
            pt = pattern[i]
            if type(st) != type(pt):
                return False, None
            elif type(st) != str:
                m, a = st.match(pt)
                if not m:
                    return False, None
                else:
                    assignment.update(a)
        if constraints.test(assignment):
            return True, assignment
        else:
            return False, None
                
    def replace(self, rules, iterations=1):
        while iterations > 0:
            i = 0
            while i < len(self):
                for rule in rules:
                    pattern = rule.pattern()
                    match, assignment = self.__local_pattern_match(i, rule)
                    if match:
                        replacement = rule.replacement(assignment)
                        for j in xrange(len(pattern)):
                            self.tokens().pop(i)
                        for j in xrange(len(replacement)):
                            self.tokens().insert(i+j, replacement[j])
                        i += len(replacement) - 1
                        continue
                i += 1
            iterations -= 1
        return self
    
    def __rotation_matrix(self, angle):
        alpha = np.radians(angle)
        return np.matrix([[np.cos(alpha), -np.sin(alpha)],
                          [np.sin(alpha),  np.cos(alpha)]])
    
    def track(self, angle, constants=["F"], start_rotation=0):
        """ track tokens as route and notice the coordinates
            F means: go one step forward
            + means: turn right
            - means: turn left
            [ means: open new childpath
            ] means: close current path move to end of the parent path """
        ltp = lambda x: 1 if x == ']' or (x.__class__ == variable and x.name() in constants) else 0
        N = sum(map(ltp, self.tokens())) + 1
        R = self.__rotation_matrix(angle)
        Rinv = np.linalg.inv(R)
        location = np.matrix([[0], [0]], dtype=float)
        delta = self.__rotation_matrix(start_rotation) * np.matrix([[0], [1]], dtype=float)
        points = np.zeros((N, 2), dtype=float)
        kinds = np.zeros(N, dtype=int)
        stack = []
        i = 1
        for turn in self.tokens():
            if turn == '[': #fork
                stack.append((np.copy(location), np.copy(delta)))
            elif turn == ']': #go back to last junction
                location, delta = stack.pop()
                points[i] = location.reshape(2)
                kinds[i] = MOVE
                i += 1
            elif turn.name() == '+': #turn right
                delta = R * delta
            elif turn.name() == '-': #turn left
                delta = Rinv * delta
            elif turn.name() in constants: #move forward
                stepsize = (turn[0].value() if len(turn) == 1 else 1)
                location += delta * stepsize
                points[i] = location.reshape(2)
                kinds[i] = LINE
                i += 1
        """ normalization """
        points[:,0] -= points[:,0].min()
        points[:,1] -= points[:,1].min()
        return points, kinds
    
    def __len__(self):
        return len(self.__tokens)
    
    def __getitem__(self, key):
        return self.__tokens[key]
    
    def __str__(self):
        T = self.__tokens
        return "".join([str(t) for t in T])
        

class pattern:
    """ pattern := pattern^* | [pattern^*] | variable_p """
    
    def __init__(self, text):
        #read tokens
        self.__tokens = []
        while len(text) > 0:
            c = text[0]
            if c == '[' or c == ']':
                self.__tokens.append(text.pop(0))
            elif (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') or c == '+' or c == '-':
                self.__tokens.append(variable(text, name))
            else:
                break
    
    def __getitem__(self, key):
        return self.__tokens[key]
    
    def __len__(self):
        return len(self.__tokens)
    
    def __str__(self):
        s = ""
        for token in self.__tokens:
            s += str(token)
        return s


class constraint:
    """ constraint := name comparator number (without spaces) """
    
    def __init__(self, text):
        self.__name = name(text)
        self.__comperator = comperator(text)
        self.__number = number(text)
    
    def name(self):
        return self.__name
    
    def comperator(self):
        return self.__comperator
    
    def number(self):
        return self.__number
    
    def test(self, number):
        return self.comperator().use(number, self.number())
    
    def __str__(self):
        return "%s%s%s" % (self.__name, self.__comperator, self.__number)
      

class constraints:
    """ constraints := constraint,constraints | constraint """
    
    def __init__(self, text):
        self.__constraints = []
        if len(text) > 0 and text[0] == ':':
            c = text.pop(0)
            while True:
                self.__constraints.append(constraint(text))
                if len(text) <= 1:
                    raise Exception("'=>' missing in pattern")
                elif text[0] == '=' and text[1] == '>':
                    break
                elif text[0] == ',':
                    text.pop(0)
                else:
                    raise Exception("%s not allowed at this position in pattern" % text[0])

    def test(self, assignment):
        for constraint in self.__constraints:
            number = assignment[str(constraint.name())]
            if not constraint.test(number):
                return False
        return True
    
    def __len__(self):
        return len(self.__constraints)
    
    def __getitem__(self, key):
        return self.__constraints[key]
    
    def __str__(self):
        return ",".join([str(c) for c in self.__constraints])


class replacement:
    """ replacement := replacement^* | [replacement^*] | variable_r """
    
    def __init__(self, text):
        self.__tokens = []
        while len(text) > 0:
            c = text[0]
            if c == '[' or c == ']':
                self.__tokens.append(text.pop(0))
            elif (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '+' or c == '-':
                self.__tokens.append(variable(text, expression))
            else:
                break
     
    def tokens(self):
        return self.__tokens 
    
    def __len__(self):
        return len(self.__tokens)
    
    def __getitem__(self, key):
        return self.__tokens[key]
    
    def __str__(self):
        T = self.__tokens
        return "".join([str(t) for t in T])


class rule:
    """ rule := pattern=>replacement """
    
    def __init__(self, text):
        if type(text) == str:
            text = list(text)
        self.__pattern = pattern(text)
        self.__constraints = constraints(text)
        c = text.pop(0)
        d = text.pop(0)
        if c != '=' or d != '>':
            raise Exception("'=>' expected in rule but '%s' found" % (c+d))
        self.__replacement = replacement(text)
    
    def pattern(self):
        return self.__pattern
    
    def constraints(self):
        return self.__constraints
        
    def replacement(self, assignment):
        T = self.__replacement.tokens()
        return [variable(t,number,assignment) if t.__class__ == variable else t for t in T]
        
    def __str__(self):
        return "%s=>%s" % (self.__pattern, self.__replacement)
            

