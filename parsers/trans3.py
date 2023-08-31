def parse_QTL(expression):
    # removing spaces for easy parsing
    expression = expression.replace(' ', '')
    operator_end = expression.find('(')
    if operator_end == -1:
        # base case: no operator found, must be a boolean variable
        print('Boolean Variable: ', expression)
    else:
        # recursive case: operator found
        operator_name = expression[:operator_end]
        if operator_name == 'prev' or operator_name == '!':
            # unary operator
            operand_start = operator_end + 1
            operand_end = len(expression) - 1  # excluding the last closing bracket
            operand = expression[operand_start:operand_end]
            print('Unary Operator: ', operator_name)
            print('Operand: ')
            parse_QTL(operand)
        elif operator_name == '&' or operator_name == 'since':
            # binary operator
            operand_start = operator_end + 1
            brackets = 0
            # finding the comma that separates the operands
            for i in range(operand_start, len(expression)):
                if expression[i] == '(':
                    brackets += 1
                elif expression[i] == ')':
                    brackets -= 1
                elif expression[i] == ',' and brackets == 0:
                    comma_pos = i
                    break
            operand1 = expression[operand_start:comma_pos]
            operand2 = expression[comma_pos+1:len(expression) - 1]  # excluding the last closing bracket
            print('Binary Operator: ', operator_name)
            print('Operand 1: ')
            parse_QTL(operand1)
            print('Operand 2: ')
            parse_QTL(operand2)
        else:
            raise ValueError('Unknown operator: ' + operator_name)


# Test the function with the provided example
parse_QTL('since(&(&(p1,p2),!(!(p3))),&(prev(p1),prev(prev(p3))))')
