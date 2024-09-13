import ast

# custom nodes for boolean operations
class BooleanAnd(ast.AST):
    _fields = ['left', 'right']

class BooleanOr(ast.AST):
    _fields = ['left', 'right']

class BooleanNot(ast.AST):
    _fields = ['operand']

class BooleanVar(ast.AST):
    _fields = ['id']

class BooleanConst(ast.AST):
    _fields = ['value']

# function to parse boolean expressions into AST
def parse_boolean_expression(expression):
    def parse_expr(tokens):
        left = parse_factor(tokens)
        while tokens and tokens[0] in {'*', '+'}:
            op = tokens.pop(0)
            right = parse_factor(tokens)
            if op == '*':
                left = BooleanAnd(left=left, right=right)
            elif op == '+':
                left = BooleanOr(left=left, right=right)
        return left

    def parse_factor(tokens):
        token = tokens.pop(0)
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

# function to print the tree
def print_tree(node, level=0):

    indent = "  " * level

    if isinstance(node, BooleanVar):
        print(f"{indent}Var: {node.id}")

    elif isinstance(node, BooleanConst):
        print(f"{indent}Const: {node.value}")

    elif isinstance(node, BooleanNot):
        print(f"{indent}Not:")
        print_tree(node.operand, level + 1)

    elif isinstance(node, BooleanAnd):
        print(f"{indent}And:")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

    elif isinstance(node, BooleanOr):
        print(f"{indent}Or:")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)

    else:
        print(f"{indent} unknown node type: {type(node)}")

# identity law: A + 0 = A   and    A * 1 = A
def apply_identity_law(node):
    if isinstance(node, BooleanOr):
        if isinstance(node.left, BooleanConst) and node.left.value == '0':
            return node.right
        
        if isinstance(node.right, BooleanConst) and node.right.value == '0':
            return node.left
        
    elif isinstance(node, BooleanAnd):
        if isinstance(node.left, BooleanConst) and node.left.value == '1':
            return node.right
        
        if isinstance(node.right, BooleanConst) and node.right.value == '1':
            return node.left
    return node

#null law: A + 1 = 1   and     A * 0 = 0
def apply_null_law(node):
    if isinstance(node, BooleanOr):
        if isinstance(node.left, BooleanConst) and node.left.value == '1':
            return node.left
        
        if isinstance(node.right, BooleanConst) and node.right.value == '1':
            return node.right
        
    elif isinstance(node, BooleanAnd):
        if isinstance(node.left, BooleanConst) and node.left.value == '0':
            return node.left
        
        if isinstance(node.right, BooleanConst) and node.right.value == '0':
            return node.right
    return node

# idempotent law: A + A = A    and      A * A = A
def apply_idempotent_law(node):
    if isinstance(node, BooleanOr) or isinstance(node, BooleanAnd):

        if isinstance(node.left, BooleanVar) and isinstance(node.right, BooleanVar):
            if node.left.id == node.right.id:
                return node.left
    return node

# inverse law: A + !A = 1  also   A * !A = 0
def apply_inverse_law(node):
    if isinstance(node, BooleanOr):
        if isinstance(node.left, BooleanVar) and isinstance(node.right, BooleanNot):
            if node.left.id == node.right.operand.id:
                return BooleanConst(value='1')
            
        if isinstance(node.right, BooleanVar) and isinstance(node.left, BooleanNot):
            if node.right.id == node.left.operand.id:
                return BooleanConst(value='1')
            
    elif isinstance(node, BooleanAnd):
        if isinstance(node.left, BooleanVar) and isinstance(node.right, BooleanNot):
            if node.left.id == node.right.operand.id:
                return BooleanConst(value='0')
            
        if isinstance(node.right, BooleanVar) and isinstance(node.left, BooleanNot):
            if node.right.id == node.left.operand.id:
                return BooleanConst(value='0')
    return node



def simplify_expression(node):
    def apply_simplification_rules(node):
        original_node = node
        node = apply_identity_law(node)
        node = apply_null_law(node)
        node = apply_idempotent_law(node)
        node = apply_inverse_law(node)
        return node, node != original_node

    iteration_limit = 15
    iterations = 0
    change = True

    while change and iterations < iteration_limit:
        node, change = apply_simplification_rules(node)
        if change:  # Only print if a change occurred
            print_tree(node)  
        iterations += 1

    if iterations == iteration_limit:
        print("simplification stopped due to iteration limit")

    return node


def main():
    while True:
        initial_expression = input("enter a Boolean algebra expression that you would like to be parsed into a tree: ")
        parsed_tree = parse_boolean_expression(initial_expression)
        print("heres the parsed Boolean expression tree:")
        print_tree(parsed_tree)
        print("simplifying the expression:")
        simplified_tree = simplify_expression(parsed_tree)
        print("heres the simplified Boolean expression tree:")
        print_tree(simplified_tree)
        continue_choice = input("do you want to parse another expression? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("exiting the parser.")
            break

if __name__ == "__main__":
    main()
