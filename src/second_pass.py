import ast
from pprint import pprint

INDENT_STEP = 2

binop_to_string = {
    ast.Add:    '+',
    ast.Sub:    '-',
    ast.Mult:   '*',
    ast.Div:    '/',
}

python_type_to_c_type = {
    'int': 'int',
    'float': 'double',
}

# scoped-symbol:
# <func/class>::<symbol>


class SecondPass(ast.NodeVisitor):
    def __init__(self, first_pass):
        self.num_arguments = 0
        self.indent_level = 0
        self.out_string = ""
        self.curr_scope = []
        self.first_pass = first_pass

    def _scoped_sym(self, symbol):
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope) + "::"
        return scope_string + symbol

    def _symbol_type(self, scoped_symbol, default=None):
        if default is None:
            return self.first_pass.types[scoped_symbol]
        else:
            return self.first_pass.types.get(scoped_symbol, default)

    def indented(self, s):
        return ' ' * self.indent_level + s

    def output(self, s, indent=False):
        if indent:
            self.out_string += self.indented(s)
        else:
            self.out_string += s
        if self.out_string[-1] == '\n':
            print(self.out_string[:-1])
            self.out_string = ''

    def print(self, s):
        print(self.indented(s))

    def indent(self):
        self.indent_level += INDENT_STEP

    def outdent(self):
        if self.indent_level >= INDENT_STEP:
            self.indent_level -= INDENT_STEP

    def visit_Module(self, node):
        self.generic_visit(node)

    def visit_AnnAssign(self, node, override_target=None):
        if override_target is None:
            target = node.target.id
        else:
            target = override_target
        scoped_sym = self._scoped_sym(target)
        t_type = self._symbol_type(scoped_sym)
        c_type = python_type_to_c_type[t_type]
        value = self.visit(node.value)
        c_assignment = f"{c_type} {target} = {value};\n"
        self.output(c_assignment, indent=True)

    def visit_Assign(self, node):
        return self.visit_AnnAssign(node, override_target=node.targets[0].id)

    def visit_Constant(self, node):
        return node.value

    def visit_arguments(self, node):
        self.num_arguments = 0
        self.output("(")
        self.generic_visit(node)
        self.output(") {\n")

    def visit_arg(self, node):
        if self.num_arguments > 0:
            self.output(", ")
        self.num_arguments += 1
        scoped_sym = self._scoped_sym(node.arg)
        if node.annotation is None:
            def_type = 'int'
        else:
            def_type = node.annotation.id
        sym_type = self._symbol_type(scoped_sym, default=def_type)
        self.output(f"{sym_type} {node.arg}")
        self.generic_visit(node)

    def visit_Name(self, node):
        self.generic_visit(node)

    def visit_Load(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        funcname = node.name
        self.output(f"\nint {funcname}")
        self.curr_scope.append(node.name)
        self.indent()
        self.generic_visit(node)
        self.outdent()
        self.curr_scope.pop(len(self.curr_scope)-1)
        self.output("}\n\n\n")

    def visit_Expr(self, node):
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            self.output(node.func.value.id + "." + node.func.attr, indent=True)
        else:
            self.output(node.func.id, indent=True)
        self.output("(")
        if len(node.args) > 0:
            self.num_arguments = 0
            for arg in node.args:
                if self.num_arguments > 0:
                    self.output(", ")
                self.num_arguments += 1
                if isinstance(arg, ast.Constant):
                    value = self.visit(arg)
                    if isinstance(value, str):
                        value = f'"{value}"'
                elif isinstance(arg, ast.Name):
                    value = arg.id
                elif isinstance(arg, ast.BinOp):
                    l_value = self.visit(arg.left)
                    r_value = self.visit(arg.right)
                    op_s = binop_to_string[arg.op.__class__]
                    value = f"{l_value} {op_s} {r_value}"
                else:
                    raise Exception(f"Unexpected {arg=}")
                self.output(f"{value}")
        self.output(");\n")

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if visitor == self.generic_visit:
            print(f"Would call {method} {node!r}")
        return visitor(node)
