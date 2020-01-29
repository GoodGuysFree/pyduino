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

    def _current_scope(self):
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope)
        return scope_string

    def _scoped_sym(self, symbol):
        scope_string = self._current_scope()
        if len(self.curr_scope) > 0:
            scope_string += "::"
        return scope_string + symbol

    def _symbol_type(self, scoped_symbol, default=None):
        if default is None:
            return self.first_pass.types[scoped_symbol]
        else:
            return self.first_pass.types.get(scoped_symbol, default)

    def _local_name(self, scoped_var_name):
        if scoped_var_name.find('::') > 0:
            parts = scoped_var_name.split('::')
            return parts[-1]
        else:
            return scoped_var_name

    def indented(self, s):
        return ' ' * self.indent_level + s

    def output(self, s, indent=False):
        if indent:
            if '\n' in s.rstrip('\n'):
                lines = [self.indented(x).rstrip() for x in s.splitlines()]
                line = "\n".join(lines)
                if len(s) > 0 and s[-1] == '\n':
                    line += '\n'
                self.out_string += line
            else:
                self.out_string += self.indented(s)
        else:
            self.out_string += s
        if len(self.out_string) > 0 and self.out_string[-1] == '\n':
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
        c_assignment = f"{target} = {value};\n"
        self.output(c_assignment, indent=True)

    def visit_Assign(self, node):
        return self.visit_AnnAssign(node, override_target=node.targets[0].id)

    def visit_Constant(self, node):
        return node.value

    def emit_local_variables(self, node):
        local_vars = self.first_pass.find_local_vars(self._current_scope())
        if local_vars:
            self.output("/* Local Variable Declarations */\n", indent=True)
            for var_name in local_vars:
                v_type = self._symbol_type(var_name)
                c_type = python_type_to_c_type[v_type]
                v_name = self._local_name(var_name)
                self.output(f"{c_type} {v_name};\n", indent=True)
            self.output("\n")

    def visit_arguments(self, node):
        self.num_arguments = 0
        self.output("(")
        self.generic_visit(node)
        self.output(") {\n")
        self.emit_local_variables(node)
        self.output("/* Main Code */\n", indent=True)

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
        return node.id

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

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op_s = binop_to_string[node.op.__class__]
        right = self.visit(node.right)
        return f"({left} {op_s} {right})"

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
                    value = self.visit_BinOp(arg)
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
