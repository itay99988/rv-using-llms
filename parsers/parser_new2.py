from pyparsing import Word, alphas, Forward, opAssoc, infixNotation, nums, Group, oneOf

# Definition of the elements
operand = Word(alphas+nums)
operator = oneOf("&& || ! -> <-> S H O P")

# Creating a parser
class Node:
    def __init__(self, tokens):
        self.tokens = tokens

class UnaryNode(Node):
    def __init__(self, tokens):
        Node.__init__(self, tokens)
        self.op = tokens[0][0]
        self.operand = tokens[0][1]

class BinaryNode(Node):
    def __init__(self, tokens):
        Node.__init__(self, tokens)
        self.left = tokens[0][0]
        self.op = tokens[0][1]
        self.right = tokens[0][2]

# Grammar definition
formula = Forward()

# Defining the grammar of the formula
formula << infixNotation(operand,
    [
        ("H", 1, opAssoc.RIGHT, UnaryNode),
        ("O", 1, opAssoc.RIGHT, UnaryNode),
        ("P", 1, opAssoc.RIGHT, UnaryNode),
        ("!", 1, opAssoc.RIGHT, UnaryNode),
        ("&&", 2, opAssoc.LEFT, BinaryNode),
        ("||", 2, opAssoc.LEFT, BinaryNode),
        ("->", 2, opAssoc.LEFT, BinaryNode),
        ("<->", 2, opAssoc.LEFT, BinaryNode),
        ("S", 2, opAssoc.LEFT, BinaryNode)
    ])

def formula_to_ast(formula_string):
    return formula.parseString(formula_string, parseAll=True)[0]

def ast_to_string(ast):
    if isinstance(ast, UnaryNode):
        return f"{ast.op}({ast_to_string(ast.operand)})"
    elif isinstance(ast, BinaryNode):
        return f"({ast_to_string(ast.left)} {ast.op} {ast_to_string(ast.right)})"
    else:
        return ast

ast = formula_to_ast("q5 || (P(q3) -> O(q7))")
print(ast_to_string(ast))  # prints: (q5 || (P(q3) -> O(q7)))
