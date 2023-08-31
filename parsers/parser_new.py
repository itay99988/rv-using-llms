import re

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class And(BinOp):
    pass

class Or(BinOp):
    pass

class Imp(BinOp):
    pass

class BiImp(BinOp):
    pass

class S(BinOp):
    pass

class Not:
    def __init__(self, child):
        self.child = child

class UnaryOp:
    def __init__(self, child):
        self.child = child

class H(UnaryOp):
    pass

class O(UnaryOp):
    pass

class P(UnaryOp):
    pass

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

def lexer(input_string):
    token_specs = [
        ("VAR",   r"q\d+"),
        ("AND",   r'&&'),
        ("OR",    r'\|\|'),
        ("NOT",   r'!'),
        ("IMP",   r'->'),
        ("BIIMP", r'<->'),
        ("S",     r'S'),
        ("H",     r'H'),
        ("O",     r'O'),
        ("P",     r'P'),
        ("LPAR",  r'\('),
        ("RPAR",  r'\)'),
        ("SKIP",  r'\s+'),  # Skip over spaces and tabs
        ("MISMATCH", r'.')  # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    for mo in re.finditer(tok_regex, input_string):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        elif kind != 'SKIP':
            yield Token(kind, value)

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def formula(self):
        """ Parse a formula """
        left = self.term()

        if self.pos < len(self.tokens) and self.tokens[self.pos].type == "IMP":
            self.pos += 1
            right = self.formula()
            return Imp(left, right)

        if self.pos < len(self.tokens) and self.tokens[self.pos].type == "BIIMP":
            self.pos += 1
            right = self.formula()
            return BiImp(left, right)

        return left

    def term(self):
        """ Parse a term """
        left = self.factor()

        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ["AND", "OR", "S"]:
            if self.tokens[self.pos].type == "AND":
                self.pos += 1
                right = self.factor()
                left = And(left, right)
            elif self.tokens[self.pos].type == "OR":
                self.pos += 1
                right = self.factor()
                left = Or(left, right)
            elif self.tokens[self.pos].type == "S":
                self.pos += 1
                right = self.factor()
                left = S(left, right)

        return left

    def factor(self):
        """ Parse a factor """
        if self.tokens[self.pos].type in ["NOT", "H", "O", "P"]:
            op_type = self.tokens[self.pos].type
            self.pos += 1
            child = self.factor()
            if op_type == "NOT":
                return Not(child)
            elif op_type == "H":
                return H(child)
            elif op_type == "O":
                return O(child)
            elif op_type == "P":
                return P(child)

        elif self.tokens[self.pos].type == "VAR":
            var_name = self.tokens[self.pos].value
            self.pos += 1
            return Var(var_name)

        elif self.tokens[self.pos].type == "LPAR":
            self.pos += 1
            inner_formula = self.formula()
            if self.tokens[self.pos].type != "RPAR":
                raise RuntimeError("Expected )")
            self.pos += 1
            return inner_formula

def formula_to_ast(formula_string):
    tokens = lexer(formula_string)
    parser = Parser(tokens)
    return parser.formula()

def ast_to_string(ast):
    if isinstance(ast, Var):
        return ast.name
    elif isinstance(ast, And):
        return f'({ast_to_string(ast.left)} && {ast_to_string(ast.right)})'
    elif isinstance(ast, Or):
        return f'({ast_to_string(ast.left)} || {ast_to_string(ast.right)})'
    elif isinstance(ast, Imp):
        return f'({ast_to_string(ast.left)} -> {ast_to_string(ast.right)})'
    elif isinstance(ast, BiImp):
        return f'({ast_to_string(ast.left)} <-> {ast_to_string(ast.right)})'
    elif isinstance(ast, S):
        return f'({ast_to_string(ast.left)} S {ast_to_string(ast.right)})'
    elif isinstance(ast, Not):
        return f'!{ast_to_string(ast.child)}'
    elif isinstance(ast, H):
        return f'H({ast_to_string(ast.child)})'
    elif isinstance(ast, O):
        return f'O({ast_to_string(ast.child)})'
    elif isinstance(ast, P):
        return f'P({ast_to_string(ast.child)})'

ast = formula_to_ast('H(q3 -> P(q4) -> P(q5))')
print(ast_to_string(ast))
