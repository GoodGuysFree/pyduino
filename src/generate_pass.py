import ast
from pprint import pprint

from scope_tracker import ScopeTracker

INDENT_STEP = 4

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


class GeneratePass(ScopeTracker):
    def __init__(self, symbols, tree, output_file):
        super().__init__()
        self.syms = symbols
        self.indent_level = 0
        self.out_string = ""
        self.outf = output_file

        # Local context stuff
        self.num_arguments = 0

        # Run the tree
        self.visit(tree)

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
            self.outf.write(self.out_string)
            self.out_string = ''

    def indent(self):
        self.indent_level += INDENT_STEP

    def outdent(self):
        if self.indent_level >= INDENT_STEP:
            self.indent_level -= INDENT_STEP

    def emit_list_decl(self, parts, symbol):
        assert len(parts) == 3
        elem_type = parts[2]
        list_size = parts[1]
        self.output(f"{elem_type} {symbol}[{list_size}];", indent=True)

    def emit_advanced_decl(self, adv_type, symbol):
        assert ':' in adv_type
        parts = adv_type.split(':')
        selector = parts[0]
        if selector == 'list':
            self.emit_list_decl(parts, symbol)
        else:
            raise Exception(f"Unknown advanced type description {adv_type=}")

    def emit_scope_local_decls(self):
        local_syms = self.syms.find_local_syms(self.current_scope())
        if len(local_syms) > 0 and self.current_scope() != "":
            self.output("/* Local Variable Declarations */\n", indent=True)
        for name in sorted(local_syms):
            local_name = self.syms.unscoped_sym(name)
            local_type = self.syms.find_type(name)
            if ':' in local_type:   # advanced types, like list:int etc.
                self.emit_advanced_decl(local_type, local_name)
            else:
                self.output(f"{local_type} {local_name};\n", indent=True)
        if len(local_syms) > 0:
            self.output("\n")

    #
    # Visit Functions
    #

    def visit_Global(self, node):
        pass

    def visit_Module(self, node):
        self.emit_scope_local_decls()
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_name = node.name
        self.output(f"\nint {func_name}")
        self.enter_scope(func_name)
        self.indent()
        self.generic_visit(node)    # visit all children of this node
        self.outdent()
        self.exit_scope(func_name)
        self.output("}\n\n\n")

    def visit_arguments(self, node):
        self.num_arguments = 0
        self.output("(")
        self.generic_visit(node)
        self.output(") {\n")
        self.emit_scope_local_decls()
        self.output("/* Main Code */\n", indent=True)

    def visit_arg(self, node):
        if self.num_arguments > 0:
            self.output(", ")
        self.num_arguments += 1
        scoped_sym = self.scoped_sym(node.arg)
        scoped_typ = self.syms.find_type(scoped_sym)
        self.output(f"{scoped_typ} {node.arg}")
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        target = node.target.id
        scoped_target = self.scoped_sym(target)
        known_type = self.syms.find_type(scoped_target)
        tgt_type = node.annotation.id
        assert known_type == tgt_type
        value = self.visit(node.value)
        self.output(f"{target} = {value};\n", indent=True)

    def visit_Assign(self, node):
        targets = node.targets
        tgt_type = self.syms.find_type(self.scoped_sym(targets[0].id))
        tgt_names = []
        for target in targets:
            tgt_name = target.id
            assert self.syms.find_type(self.scoped_sym(tgt_name)) == tgt_type
            tgt_names.append(target.id)
        tgt_s = " = ".join(tgt_names)
        value = self.visit(node.value)
        self.output(f"{tgt_s} = {value};\n", indent=True)

    def visit_Constant(self, node):
        return node.value

    def visit_List(self, node):
        s = "["
        first = True
        for elem in node.elts:
            if first:
                first = False
            else:
                s += ", "
            s += str(self.visit(elem))
        s += "]"
        return s

    def visit_Tuple(self, node):
        return self.visit_List(node)

    def visit_Name(self, node):
        return node.id

    def visit_Load(self, node):
        self.generic_visit(node)

    def visit_Expr(self, node):
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op_s = binop_to_string[node.op.__class__]
        right = self.visit(node.right)
        return f"({left} {op_s} {right})"

    def visit_UnaryOp(self, node):
        s = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            s = f"-{s}"
        return s

    def visit_Index(self, node):
        return str(self.visit(node.value))

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
                elif isinstance(arg, ast.Subscript):
                    value = self.visit(arg.value)
                    value += "["
                    value += self.visit(arg.slice)
                    value += "]"
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
