import ast #importing library to help me parse the expression

# defining custom nodes for the different operations

class BooleanAnd(ast.AST):
    _fields = ['left', 'right']  # fields for left and right operands

class BooleanOr(ast.AST):
    _fields = ['left', 'right']  # fields for left and right operands

class BooleanNot(ast.AST):
    _fields = ['operand']  # field for the operand before the !

class BooleanVar(ast.AST):
    _fields = ['id']  # Field, so variables are easily identifiable

class BooleanConst(ast.AST):
    _fields = ['value']  # Field for the constant value (0 or 1)