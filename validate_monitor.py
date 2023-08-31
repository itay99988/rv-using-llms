from pltl2nodes import formula_stats
from chat import Chat
from prompts import *

import subprocess
import random
from time import sleep

SCRIPT_NAME = "monitor.py"

# The command to run the script to be tested
command = ['python', SCRIPT_NAME]


# this function expects assignments in the format "q1=True,q2=False,q3=True" etc
def test_single_trace(assignments_lst, expected_output):
    try:
        # Start the subprocess
        subprocess_run = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, text=True)
        sleep(1)

        # send events
        for event in assignments_lst:
            subprocess_run.stdin.write(event+'\n')
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
        if num_boolean_responses != len(assignments_lst):
            print(f"Sanity check failed for the given trace: Expected {len(assignments_lst)} boolean responses, but got {num_boolean_responses}.")
            return False

        final_monitor_output = boolean_responses[-1].strip().lower() == "true"
        if final_monitor_output != expected_output:
            print(f"Validation failed for the given trace.")
            return False
        else:
            print(f"Trace validation passed: The final output was '{expected_output}' as expected.")
            return True

    except Exception as e:
        print(f"Trace validation failed: An error occurred while running the script. The error message is: {e}")
        return False


# assuming that cht is loaded with the correct nodes` context (from the abstract syntax tree)
# def nodes_to_code(cht, formula, verbose=False):
#     # getting some formula stats
#     vars_count_dict, ops_count_dict = formula_stats(formula)
#     uniq_vars_count = len(vars_count_dict.keys())
#
#     # build adaptive prompt
#     monitor_gen_prompt = build_custom_gen_prompt(formula)
#
#     success = False
#     for _ in range(cht.QUERY_LIMIT//2):
#         # monitor generation prompt
#         code_response = cht.new_message(monitor_gen_prompt)
#         if verbose: print(code_response)
#
#         if not extract_code(code_response):
#             print("Trying to generate the monitor again.")
#             cht.pop_history(2)
#             continue
#
#         if not code_sanity_check(uniq_vars_count):
#             print("Trying to generate the monitor again.")
#             cht.pop_history(2)
#             continue
#
#         # if you are here, then the checks passed
#         success = True
#         break
#
#     return success


if __name__ == "__main__":
    cht = Chat()
    trace = ["q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True",
             "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True", "q1=True"]
    test_single_trace(trace, True)
