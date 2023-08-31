from sent2pltl import sent_to_pltl
from pltl2nodes import pltl_to_nodes
from nodes2code import nodes_to_code
from chat import Chat, OldChat


def main():
    cht_translate = Chat(temperature=0.1)
    cht_generate = Chat()

    # sentence = input("Please enter a sentence: \n")
    sentence = "the robot is always at the store, and whenever it is at the garage, it cannot be at the house."

    formula, variables_dict = sent_to_pltl(cht_translate, sentence, verbose=True)
    if len(formula) == 0:
        print("Failed to translate the sentence to past-time LTL.")
        exit()

    print(f"Your sentence was successfully translated to past-time LTL:\n{formula}\n The next step -- building the AST.")

    if not pltl_to_nodes(cht_generate, formula, verbose=True):
        print("Could not translate the formula into a correct parse tree. Exiting.")
        exit()

    print("The formula was successfully converted to an abstract syntax tree. The next step -- generating the RV monitor.")

    if not nodes_to_code(cht_generate, formula, verbose=True):
        print("Could not build a valid monitor out of the parse tree. Exiting")
        exit()

    print("A monitor was successfully generated. Check out the file monitor.py")


if __name__ == "__main__":
    main()
