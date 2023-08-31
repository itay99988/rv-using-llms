from prompts import *
from chat import Chat

ATTEMPTS = 3


def extract_mod_sentence(response):
    if 'conditions: ' in response:
        reduced_body = response.split('conditions: ')[1]
        values_for_dict = reduced_body.split('\n')[0].strip().split(';')
        if response.count("#") >= 2:
            mod_sentence = reduced_body.split('\n')[1].split('#')[1].strip()
            variables_dict = {f'q{i}': values_for_dict[i - 1].strip() for i in range(1, len(values_for_dict) + 1)}
        else:
            mod_sentence, variables_dict = "", {}
    else:
        mod_sentence, variables_dict = "", {}

    return mod_sentence, variables_dict


def extract_translation(response):
    if response.count("#") >= 2:
        formula = response.split('#')[1].strip()
    else:
        formula = ""

    return formula


def sent_to_pltl(cht, sentence, verbose=False):
    formula, variables_dict = "", {}

    for _ in range(ATTEMPTS):
        cht.reset_history()
        response1 = cht.new_message(REPLACE_LANDMARKS.format(sentence))
        if verbose: print(response1)

        mod_sentence, variables_dict = extract_mod_sentence(response1)
        # if the landmarks replace failed
        if len(mod_sentence) == 0:
            continue

        # move on to translation with empty history
        cht.reset_history()
        response2 = cht.new_message(TRANSLATE.format(mod_sentence))
        if verbose: print(response2)

        formula = extract_translation(response2)
        # if the translation failed
        if len(formula) == 0:
            continue

        # if you are here, then the translation was successful, so we can break.
        break

    return formula, variables_dict


if __name__ == "__main__":
    cht = Chat()
    sentence = "the robot was at the garage at all time steps."

    formula, variables_dict = sent_to_pltl(cht, sentence, verbose=False)
