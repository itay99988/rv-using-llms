class Node:
    def __init__(self, type, children=None, variable=None):
        self.type = type
        self.variable = variable
        if children is None:
            self.children = []
        else:
            self.children = children
        self.current_value = False
        self.prev_value = False

def parse(expr):
    if expr.startswith('!'):
        return Node('!', [parse(expr[2:-1])])
    elif expr.startswith('prev'):
        return Node('prev', [parse(expr[5:-1])])
    elif expr.startswith('&'):
        lhs, rhs = split_operands(expr[2:-1])
        return Node('&', [parse(lhs), parse(rhs)])
    elif expr.startswith('since'):
        lhs, rhs = split_operands(expr[6:-1])
        return Node('since', [parse(lhs), parse(rhs)])
    else:
        return Node('var', None, expr)

def split_operands(expr):
    balance = 0
    for i, c in enumerate(expr):
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
        elif c == ',' and balance == 0:
            return expr[:i], expr[i+1:]
    raise ValueError('Invalid expression: ' + expr)

def update_tree(node, event):
    if node.type == 'var':
        node.current_value = event[node.variable]
    else:
        for child in node.children:
            update_tree(child, event)

        if node.type == '!':
            node.current_value = not node.children[0].current_value
        elif node.type == 'prev':
            node.current_value = node.children[0].prev_value
        elif node.type == '&':
            node.current_value = node.children[0].current_value and node.children[1].current_value
        elif node.type == 'since':
            node.current_value = node.children[1].current_value or (node.children[0].current_value and node.prev_value)

def update_previous_values(node):
    node.prev_value = node.current_value
    for child in node.children:
        update_previous_values(child)

# usage
root = parse('since(&(&(q1,q2),!(!(q3))),&(prev(q1),prev(prev(q3))))')

while True:
    event = input('Please enter an event: ')
    # converting string of format "q1=True,q2=False,q3=True" to a dictionary
    event = {var: val == 'True' for var, val in (pair.split('=') for pair in event.split(','))}

    update_tree(root, event)
    print(root.current_value)
    update_previous_values(root)
