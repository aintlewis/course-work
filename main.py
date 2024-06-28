import ast #importing library to help me parse the expression

# defining custom nodes for the different operations

class BooleanAnd(ast.AST):
    _fields = ['left', 'right']  # fields for left and right operands

class BooleanOr(ast.AST):
    _fields = ['left', 'right']  # fields for left and right operands

class BooleanNot(ast.AST):
    _fields = ['operand']  # field for the operand next to the '!'

class BooleanVar(ast.AST):
    _fields = ['id']  # Field, so variables are easily identifiable, it will say like "var"

class BooleanConst(ast.AST):
    _fields = ['value']  # Field for the constant value (0 or 1)


# Helper function to parse boolean expressions into AST
def parse_boolean_expression(expression):

    def parse_expr(tokens): # parse full stuff w * or + 
        left = parse_factor(tokens) # parse the left operand
        while tokens and tokens[0] in {'*', '+'}: # while there are tokens left and the next token is either '*' or '+'
            op = tokens.pop(0) # pop the token
            right = parse_factor(tokens) # parse the righer operand
            if op == '*': # if it's a * it's an and
                left = BooleanAnd(left=left, right=right) # create a new node with the left and right operands
            elif op == '+': # if it an + it's an or 
                left = BooleanOr(left=left, right=right) # # create new node with left n right operands
        return left
    
    def parse_factor(tokens): # responsible for parsing the smallest units of the boolean expression
                               #e.g. variables, constants, NOT operations, and sub-expressions within parentheses.

        token = tokens.pop(0)  # Get the next token 

        if token == '!':
            operand = parse_factor(tokens)
            return BooleanNot(operand=operand)
        
        elif token == '(':
            expr = parse_expr(tokens)
            tokens.pop(0)  # Remove ')'
            return expr
        elif token in {'0', '1'}:
            return BooleanConst(value=token)
        else:
            return BooleanVar(id=token)
    tokens = list(expression.replace(' ', ''))
    return parse_expr(tokens)