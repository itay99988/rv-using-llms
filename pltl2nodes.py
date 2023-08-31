from prompts import *
from chat import Chat


def formula_stats(formula):
    ops = ["!","&&","||","->","->","<->","S","H","O","P"]
    # how many variables are there
    idx = 0
    while (f"q{idx+1}" in formula):
        idx += 1

    # variable_count_dict
    vars_count = {f"q{i}": formula.count(f"q{i}") for i in range(1, idx+1)}
    ops_count = {op: formula.count(op) for op in ops}

    return vars_count, ops_count


def consistent_ops(ops_count_dict, node_equations):
    for op in list(ops_count_dict.keys()):
        if ops_count_dict[op] != node_equations.count(op):
            return False
    return True


def pltl_to_nodes(cht, formula, verbose=False):
    success = False

    # getting some formula stats
    vars_count_dict, ops_count_dict = formula_stats(formula)
    uniq_vars_count = len(vars_count_dict.keys())
    vars_count = sum(vars_count_dict.values())
    ops_count = sum(ops_count_dict.values())
    # print(f"number of vars: {vars_count_dict}, number of ops:{ops_count_dict}")

    for _ in range(cht.QUERY_LIMIT//2):
        cht.reset_history()
        response1 = cht.new_message(BUILD_AST.format(formula))
        if verbose: print(response1)
        response2 = cht.new_message(TREE_TO_NODES)
        if verbose: print(response2)

        # count node equations
        if "#####" in response2:
            node_equations = response2.split("#####")[1]
            node_count = node_equations.count("=")
            # check if total number of nodes in the ast equals vars_count+ops_count
            if node_count != uniq_vars_count + ops_count:
                print("total nodes in the ast does not equal vars_count+ops_count")
                continue

            # check if number of operator nodes is consistent with the formula
            if not consistent_ops(ops_count_dict, node_equations):
                print("inconsistent number of operators")
                continue

            response3 = cht.new_message(TREE_VALIDATION)
            if verbose: print(response3)
            if "leaves count:" in response3:
                gpt_leaf_count = int(response3.split("leaves count:")[1].split("\n")[0].strip())
                if vars_count != gpt_leaf_count:
                    print("number of tree leaves is inconsistent with number of variable appearances.")
                    continue

                # if the above checks have passed, then break the loop. in any other case, try again
                success = True
                break

    return success


if __name__ == "__main__":
    cht = Chat()
    formula = "q1 && P(q1)"

    pltl_to_nodes(cht, formula)
