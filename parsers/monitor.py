class Node:
    def __init__(self, operator, operand1=None, operand2=None):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.current_value = False
        self.prev_value = False

    def update(self, event):
        if self.operator in {"p1", "p2", "p3"}:
            self.current_value = event[self.operator]
        elif self.operator == "!":
            self.current_value = not self.operand1.current_value
        elif self.operator == "prev":
            self.current_value = self.operand1.prev_value
        elif self.operator == "&":
            self.current_value = self.operand1.current_value and self.operand2.current_value
        elif self.operator == "since":
            self.current_value = self.operand2.current_value or (self.operand1.current_value and self.prev_value)

    def sync_prev(self):
        self.prev_value = self.current_value


node1 = Node("p1")
node2 = Node("p2")
node3 = Node("p3")
node4 = Node("prev", node3)
node5 = Node("prev", node4)
node6 = Node("!", node3)
node7 = Node("!", node6)
node8 = Node("&", node1, node2)
node9 = Node("&", node8, node7)
node10 = Node("prev", node1)
node11 = Node("&", node10, node5)
node12 = Node("since", node9, node11)

nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12]

event_sequence = [
    (True, True, False), (False, True, True), (True, False, True), (False, False, False), (True, True, True),
     (False, True, False), (True, False, False), (False, True, True), (True, False, True), (False, False, False)
]

for ev in event_sequence:
    event = {"p1": ev[0], "p2": ev[1], "p3": ev[2]}
    idx = 0
    for node in nodes:
        idx += 1
        node.update(event)
        print(f"The value of node{idx}:{node.current_value}")

    for node in nodes:
        node.sync_prev()

    print("Current value of root node: ", node12.current_value)
    print()
