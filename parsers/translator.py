class Node:
    def __init__(self, name, val, left=None, right=None):
        self.name = name
        self.val = val
        self.left = left
        self.right = right
        self.node_type = 'Boolean Variable' if left is None else 'Operator'
        self.operands = []
        if left is not None:
            self.operands.append(left.name)
        if right is not None:
            self.operands.append(right.name)
        self.current = False
        self.prev = False

    def set_current(self, event):
        if self.node_type == 'Boolean Variable':
            self.current = event.get(self.val, False)
        elif self.val == '!':
            self.current = not self.left.current
        elif self.val == 'prev':
            self.current = self.left.prev
        elif self.val == '&':
            self.current = self.left.current and self.right.current
        elif self.val == 'since':
            self.current = self.right.current or (self.left.current and self.prev)

node_counter = 0

def tokenize(expression):
    tokens = expression.split('(')
    new_tokens = []
    for token in tokens:
        new_tokens.extend(token.replace(')', ' ').replace(',', ' ').split())
    return new_tokens

def parse(tokens):
    global node_counter
    if not tokens:
        return None
    val = tokens.pop(0)
    if val in ('!', 'prev'):
        node_counter += 1
        return Node("Node" + str(node_counter), val, left=parse(tokens))
    elif val in ('&', 'since'):
        node_counter += 1
        return Node("Node" + str(node_counter), val, left=parse(tokens), right=parse(tokens))
    else:
        node_counter += 1
        return Node("Node" + str(node_counter), val)

def post_order_update_current(node, event):
    if node is None:
        return
    post_order_update_current(node.left, event)
    post_order_update_current(node.right, event)
    node.set_current(event)

def post_order_update_prev(node):
    if node is None:
        return
    post_order_update_prev(node.left)
    post_order_update_prev(node.right)
    node.prev = node.current

def analyze_qtl(expression):
    global node_counter
    node_counter = 0
    tokens = tokenize(expression)
    tree = parse(tokens)
    return tree

def print_tree(node):
    if node is None:
        return
    print_tree(node.left)
    print_tree(node.right)
    if node.node_type == 'Operator':
        print(node.name, '=', node.val + '(' + ','.join(node.operands) + ')')
    else:
        print(node.name, '=', node.val)

expression = "since(&(&(p1,p2),!(!(p3))), &(prev(p1),prev(prev(p3))))"
tree = analyze_qtl(expression)
# print_tree(tree)
while True:
    event_str = input("Enter an event: ")
    event = {k: v == 'True' for k, v in (s.split('=') for s in event_str.split(','))}
    post_order_update_current(tree, event)
    post_order_update_prev(tree)
    print(tree.current)