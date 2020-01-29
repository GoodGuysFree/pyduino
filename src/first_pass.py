import ast
from pprint import pprint

# scoped-symbol:
# <func/class>::<symbol>


class FirstPass(ast.NodeVisitor):
    def __init__(self):
        self.symbols = set()    # keeps scoped symbols
        self.types = {}         # key = symbol, value = python type annotation
        self.classes = {}
        self.funcs = {}
        self.func_args = set()
        self.curr_scope = []

    def _scoped_sym(self, symbol):
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope) + "::"
        return scope_string + symbol

    def _symbol_type(self, scoped_symbol, default=None):
        if default is None:
            return self.types[scoped_symbol]
        else:
            return self.types.get(scoped_symbol, default)

    def find_local_vars(self, scope):
        local_vars_and_args = [x for x in self.symbols if x.startswith(f"{scope}::")]
        local_vars = [x for x in local_vars_and_args if x not in self.func_args]
        return sorted(local_vars)

    def visit_AnnAssign(self, node, implicit_type=None):
        try:
            target = node.target.id
        except AttributeError:
            target = node.targets[0].id
        if implicit_type is None:
            t_type = node.annotation.id
        else:
            t_type = implicit_type
        scoped_sym = self._scoped_sym(target)
        prev_type = self._symbol_type(scoped_sym, t_type)
        if prev_type != t_type:
            raise Exception(f"In line {node.lineno}: Symbol {scoped_sym} previously defined as {prev_type}, and now as {t_type}")
        self.types[scoped_sym] = t_type
        self.symbols.add(scoped_sym)
        self.generic_visit(node)

    def visit_Assign(self, node):
        target = node.targets[0].id
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope) + "::"
        scoped_sym = scope_string + target
        t_type = self.types.get(scoped_sym, "int")
        self.visit_AnnAssign(node, implicit_type=t_type)

    def visit_FunctionDef(self, node):
        self.curr_scope.append(node.name)
        self.generic_visit(node)
        self.funcs[node.name] = 'int'   # TODO: default return type for now
        self.curr_scope.pop(len(self.curr_scope)-1)

    def visit_arguments(self, node):
        self.generic_visit(node)

    def visit_Pass(self, node):
        self.generic_visit(node)

    def visit_arg(self, node):
        scoped_sym = self._scoped_sym(node.arg)
        if node.annotation is None:
            prev_type = self._symbol_type(scoped_sym, default='int')
            t_type = prev_type
        else:
            prev_type = self._symbol_type(scoped_sym, node.annotation.id)
            t_type = node.annotation.id
        if prev_type != t_type:
            raise Exception(f"In line {node.lineno}: Symbol {scoped_sym} previously defined as {prev_type}, and now as {t_type}")
        self.types[scoped_sym] = t_type
        self.symbols.add(scoped_sym)
        self.func_args.add(scoped_sym)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.generic_visit(node)

    def visit_Load(self, node):
        self.generic_visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        #if visitor == self.generic_visit:
        #    print(f"Would call {method} {node!r}")
        return visitor(node)

    def report(self):
        pprint(self.types)
