################################################# Sent2PLTL #################################################

REPLACE_LANDMARKS = """
Your task is to repeat exact strings that refer to landmarks or conditions of an object from a given utterance, and then replace each landmark or condition with a different variable. the variables are q1, q2, q3 etc. After identifying the landmarks or conditions, write the modified sentence inside hashtags. You are provided with the following three examples:

  1. utterance: the robot had to go to the repair station, and then to the charging station.
  Landmarks/conditions: the repair station; the charging station.
  new sentence: #the robot had to go to q1, and then to q2.#

  2. utterance: the vehicle should start at the garage, then go to the grocery store and finally head back to the garage.
  Landmarks/conditions: the garage; the grocery store.
  new sentence: #the vehicle should start q1, then go to q2 and finally head back to q1.#

  3. The phone must always be on silent mode, and eventually should receive an MMS message.
  Landmarks/conditions: be on silent mode; receive an MMS message
  new sentence: #The phone must always q1, and eventually should q2.#

  now, your task is to consider the following sentence:
  "{0}".
"""


TRANSLATE = """
Your task is to translate the below natural language sentence into a past-time LTL formula and explain your translation step by step. Remember that P means "in the last step"/"in the previous timestep", S means "since", H means "historically" and O means "in the past"/"once". The formula should only contain atomic propositions or operators &&, ||, !, ->, <->, P, S, H, O. The atomic propositions would be q1, q2, q3 etc. Imporatant note: do not use the "globally" (G) operator from LTL, instead, use the H operator ("always in the past", "historically").
The "S" operator should be used in the following way:
natural language: "the robot was previously at q2, but since then it was always at q1." 
past-time LTL formula: " q1 S q2 ".

You are provided with three simple examples:
1.	natural language: "The robot was at q1 at all times."
	past-time LTL formula: # H(q1) #.
2.	natural language: "Whenever the robot is was at q1, it is not at q2."
	past-time LTL formula: # H(q1 -> !(q2)) #.
3.	natural language: "In the past, the robot was at q3."
	past-time LTL formula: # O(q3) #.
	
write your final answer inside hashtags.

please translate this sentence: "{0}"
"""

################################################# PLTL2nodes #################################################

FIRST_ANALYSIS = """
past-time linear temporal logic is a language with q1,q2,...qn as boolean variables. "!", "P","H","O" are unary operators, while "&&", "||", "->", "<->", "S" are binary operators in this language. 

Given a valid expression in this language, your task two parts:
1. How many boolean variables appearances are in the formula? if the same variable appeared multiple times, treat it as multiple appearances.
2. How many appearances of operators are in the formula? if the same operator appeared multiple times, treat it as multiple appearances.

you may provide step by step explanations to your answers, but eventually you should write your final answers in the following format:

1. boolean variables appearances: <number>
2. operators appearances: <number>

the expression is given inside backticks:

"""

BUILD_AST = """
Past-time linear temporal logic is a language with q1,q2,...qn as boolean variables. "!", "P","H","O" are unary operators, while "&&", "||", "->", "<->", "S" are binary operators in this language. 

Given a valid expression in this language, your task is to generate the abstract syntax tree of it.
Do it for the following expression inside the backticks: `{0}`. 
generate the abstract syntax tree tree while meeting the following requirements:
-do not attach unary nodes to the leaves.
-every node in the tree must have two children at most.
"""

TREE_TO_NODES = """
Your next task has two steps, given the same expression in this language:
1.	Name every leaf and non-leaf node in the tree. The name format should be "node{index}", where an ascending index would be in the placeholder. Start from bottom to top. The first nodes should be the leaves. If two leaves represent the same boolean variable, give them the same name. 
2.	Describe every node with the operator it represents and with one or two of its immediate descendants. For example: "node2 = node3 && node6". If the node is a leaf node, describe it as "node{index}=q1 if its corresponding boolean variable is q1. 
    The order of the statements is important: you can use a certain node as an operand in a statement only if its associated statement was already written. You should finish with the root of the tree.
    please use the following format:
    #####
    <node description>
    <node description>
    ...
    #####
"""

TREE_VALIDATION = """
Your next task is to count the number of leaves in the abstract syntax tree.
please write your final answer in the following format:

leaves count: <number>
"""

################################################# nodes2code #################################################

MONITOR_GEN_FULL = """
Your final task is to generate a Python program that receives at each step an assignment for all the Boolean variables in the above Past-time linear temporal logic expression, and then prints an output. This assignment of the Boolean variables is referred to as an event. At each step, the event would be inserted by the user. The output will be based on a certain analysis of the event. The program would then be ready to receive another event from the user and analyze it in a similar manner, and finally print another output, and so forth. The Program would terminate when the user inserted the word "abort". 
To perform the analysis, we would keep in memory two versions of the values of each node from the previous task. The first version would be the current version while the other one would be the previous version. Before the first step, the current version of all nodes can be assumed to be a "False" value, except of the current version of an "H" node that should be initialized to "True".
The current version of each node will be updated based on its type and on its previous version. The update order of the nodes should be the same as in the previous task - node's current version may be updated only after its operands are updated.
-   A leaf node would be the truth value of the corresponding variable according to the new event.
-	The current version of node of type "!" would be the negation of the current version of its single operand.
-	The current version of node of type "&&" would be an "and" conjunction between the current versions of its two operands.
-	The current version of node of type "||" would be an "or" disjunction between the current versions of its two operands.
-	The current version of node of type "->" would be an "or" disjunction between the negation of the current version of its left operand, and its right operand.
-	The current version of node of type "<->" would be "True" if the current versions of both of its operands are equal, and "False" otherwise.
-	The current version of node of type "P" would be the previous version of its operand.
-	The current version of node of type "S" would be an "or" disjunction between two terms. The first term would be the current versions of the right operand of the node, while the second term would be an "and" conjunction between the current version of the left operand of the node, and the previous version of the node itself.
-	The current version of node of type "O" would be an "or" disjunction between the current version of its single operand, and the previous version of the node itself.
-	The current version of node of type "H" would be an "and" conjunction between the current version of its single operand, and the previous version of the node itself.

The previous version of all nodes will be updated only after the current version of all nodes is updated. Finally, the current version of the root node should be printed.

-When asking the user for an event, you must not print anything to the user, just expect an input of the format "q1=<boolean>,q2=<boolean>,....", where "boolean" is either "True" or "False".
-When printing the current version of the root node, print just a single word that describes its boolean value (True or False).
"""

MONITOR_GEN = """
Your final task is to generate a Python program that receives at each step an assignment for all the Boolean variables in the above Past-time linear temporal logic expression, and then prints an output. This assignment of the Boolean variables is referred to as an event. At each step, the event would be inserted by the user. The output will be based on a certain analysis of the event. The program would then be ready to receive another event from the user and analyze it in a similar manner, and finally print another output, and so forth. The Program would terminate when the user inserted the word "abort". 
To perform the analysis, we would keep in memory two versions of the values of each node from the previous task. The first version would be the current version while the other one would be the previous version. Before the first step, the current version of all nodes can be assumed to be a "False" value, except of the current version of an "H" node that should be initialized to "True".
The current version of each node will be updated based on its type and on its previous version. The update order of the nodes should be the same as in the previous task - node's current version may be updated only after its operands are updated.
- A leaf node would be the truth value of the corresponding variable according to the new event.
{0}
The previous version of all nodes will be updated only after the current version of all nodes is updated. Finally, the current version of the root node should be printed.

-When asking the user for an event, you must not print anything to the user, just expect an input of the format "q1=<boolean>,q2=<boolean>,....", where "boolean" is either "True" or "False".
-When printing the current version of the root node, print just a single word that describes its boolean value (True or False).
"""

MONITOR_GEN_OP_DICT = {
    "!": f"- The current version of node of type '!' would be the negation of the current version of its single operand.",
    "&&": f"- The current version of node of type '&&' would be an 'and' conjunction between the current versions of its two operands.",
    "||": f"- The current version of node of type '||' would be an 'or' disjunction between the current versions of its two operands.",
    "->": f"- The current version of node of type '->' would be an 'or' disjunction between the negation of the current version of its left operand, and its right operand.",
    "<->": f"- The current version of node of type '<->' would be 'True' if the current versions of both of its operands are equal, and 'False' otherwise.",
    "P": f"- The current version of node of type 'P' would be the previous version of its operand.",
    "S": f"- The current version of node of type 'S' would be an 'or' disjunction between two terms. The first term would be the current versions of the right operand of the node, while the second term would be an 'and' conjunction between the current version of the left operand of the node, and the previous version of the node itself.",
    "O": f"- The current version of node of type 'O' would be an 'or' disjunction between the current version of its single operand, and the previous version of the node itself.",
    "H": f"- The current version of node of type 'H' would be an 'and' conjunction between the current version of its single operand, and the previous version of the node itself."
}
