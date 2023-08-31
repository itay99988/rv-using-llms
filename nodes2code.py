from pltl2nodes import formula_stats
from chat import Chat
from prompts import *

import subprocess
import random
from time import sleep

SEQ_LEN = 20
SCRIPT_NAME = "monitor.py"

# The command to run the script to be tested
command = ['python', SCRIPT_NAME]


def build_custom_gen_prompt(formula):
    ops = ["!", "&&", "||", "->", "<->", "S", "H", "O", "P"]
    ops_instructions = ""

    for op in ops:
        if op in formula:
            ops_instructions += MONITOR_GEN_OP_DICT[op] + "\n"

    return MONITOR_GEN.format(ops_instructions)


def extract_code(gpt_response):
    if "```" in gpt_response and "python\n" in gpt_response:
        code_str = gpt_response.split("```")[1].split("python\n")[1]

        # save the code
        f = open(SCRIPT_NAME, "w")
        f.write(code_str)
        f.close()

        print("Monitor code was successfully extracted")
        return True

    print("could not extract the code from the LLMs message.")
    return False


def code_sanity_check(var_count):
    try:
        # Start the subprocess
        subprocess_run = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, text=True)
        sleep(1)

        # Define ten events and send them to the script
        for i in range(SEQ_LEN):
            event_prompt = ""
            for idx in range(1, var_count+1):
                event_prompt += f"q{idx}={random.choice(['True', 'False'])},"
            # replace last char with \n
            event_prompt = event_prompt[:-1] + "\n"

            subprocess_run.stdin.write(event_prompt)
            subprocess_run.stdin.flush()

        # Send "abort" to the script to end it
        subprocess_run.stdin.write("abort\n")
        subprocess_run.stdin.flush()

        # Get the output of the script
        output, error = subprocess_run.communicate()

        # Split the output into lines
        output_lines = output.splitlines()

        # Check the number of boolean responses
        boolean_responses = [line for line in output_lines if line.lower() in ['true', 'false']]
        num_boolean_responses = len(boolean_responses)

        # Report if the number of responses is not as expected
        if num_boolean_responses != SEQ_LEN:
            print(f"Sanity check failed: Expected {SEQ_LEN} boolean responses, but got {num_boolean_responses}.")
            return False
        else:
            print(f"Sanity check passed: Received {SEQ_LEN} boolean responses as expected.")
            return True

    except Exception as e:
        print(f"Sanity check failed: An error occurred while running the script. The error message is: {e}")
        return False


# assuming that cht is loaded with the correct nodes` context (from the abstract syntax tree)
def nodes_to_code(cht, formula, verbose=False):
    # getting some formula stats
    vars_count_dict, ops_count_dict = formula_stats(formula)
    uniq_vars_count = len(vars_count_dict.keys())

    # build adaptive prompt
    monitor_gen_prompt = build_custom_gen_prompt(formula)

    success = False
    for _ in range(cht.QUERY_LIMIT//2):
        # monitor generation prompt
        code_response = cht.new_message(monitor_gen_prompt)
        if verbose: print(code_response)

        if not extract_code(code_response):
            print("Trying to generate the monitor again.")
            cht.pop_history(2)
            continue

        if not code_sanity_check(uniq_vars_count):
            print("Trying to generate the monitor again.")
            cht.pop_history(2)
            continue

        # if you are here, then the checks passed
        success = True
        break

    return success


if __name__ == "__main__":
    cht = Chat()
    formula = "&& || -> <-> SHOP!"
