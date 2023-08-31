class Node:
    def __init__(self, name, operator=None):
        self.name = name
        self.operator = operator
        self.current_value = False
        self.previous_value = False
        self.children = []

    def update_current_value(self):
        if self.operator is None:
            return
        if self.operator == "O":
            self.current_value = any(child.current_value for child in self.children)

    def update_previous_value(self):
        self.previous_value = self.current_value

def parse_event(event):
    assignments = event.strip().split(',')
    variable_dict = {}
    for assignment in assignments:
        key, value = assignment.split('=')
        variable_dict[key.strip()] = (value.strip() == "True")
    return variable_dict

def evaluate_tree(root_node, variable_dict):
    if root_node.operator is None:
        root_node.current_value = variable_dict[root_node.name]
    else:
        for child in root_node.children:
            evaluate_tree(child, variable_dict)
        root_node.update_current_value()

def main():
    node1 = Node("q1")
    node2 = Node("O", operator="O")
    node2.children.append(node1)

    root = node2

    while True:
        event = input()
        if event.lower() == "abort":
            break

        variable_dict = parse_event(event)
        evaluate_tree(root, variable_dict)

        # Update the previous values after evaluating the current values of all nodes
        for node in [node1, node2]:
            node.update_previous_value()

        print("True" if root.current_value else "False")

if __name__ == "__main__":
    main()
