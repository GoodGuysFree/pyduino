import ast
from pprint import pprint

# scoped-symbol:
# <func/class>::<symbol>


class SymbolPass(ast.NodeVisitor):
    def __init__(self, tree):
        self.curr_scope = []
        self.symbols = {}  # key = scope, value = set of scoped symbol-names in this scope
        self.types = {}    # key = scoped-symbol, value = python type
        self.visit(tree)

    def current_scope(self):
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope)
        return scope_string

    def scoped_sym(self, symbol):
        if symbol.find('::') >= 0:
            return symbol
        scope_string = self.current_scope()
        if len(self.curr_scope) > 0:
            scope_string += "::"
        return scope_string + symbol

    def enter_scope(self, scope):
        self.curr_scope.append(scope)

    def exit_scope(self, scope):
        assert self.curr_scope[-1] == scope
        self.curr_scope = self.curr_scope[:-1]

    def get_type_from_value(self, value_node):
        if isinstance(value_node, ast.Constant):
            value = value_node.value
            if isinstance(value, int):
                return 'int'
            elif isinstance(value, str):
                raise Exception("Strings not yet supported")
            elif isinstance(value, float):
                return 'float'
            else:
                raise Exception(f"Unexpected value type: {value}")
        else:
            raise Exception(f"Unexpected value_node type: {value_node}")

    def add_symbol_to_scope(self, symbol, scope=None):
        if scope is None:
            this_scope = self.current_scope()
        else:
            this_scope = scope
        scope_symbols = self.symbols.get(this_scope, set())
        scope_symbols.add(symbol)
        self.symbols[this_scope] = scope_symbols

    def is_known_in_scope(self, symbol, scope=None):
        if scope is None:
            this_scope = self.current_scope()
        else:
            this_scope = scope
        return symbol in self.symbols.get(this_scope, set())

    def is_known_global(self, symbol):
        return self.is_known_in_scope(symbol, self.current_scope())

    def add_scoped_symbol_type(self, s_name, s_type):
        scoped_sym = self.scoped_sym(s_name)
        assert scoped_sym not in self.types
        self.types[scoped_sym] = s_type

    def visit_Global(self, node):
        this_scope = self.current_scope()
        this_scope_symbols = self.symbols.get(this_scope, set())
        this_scope_symbols.update(node.names)
        self.symbols[this_scope] = this_scope_symbols

    def visit_Assign(self, node):
        '''Assignment without annotation:
           Check if symbol is new or existing.
           If existing, try to check if the type is the same. In C we can't change types...'''
        for target in node.targets:
            tgt_id = target.id
            tgt_ty = self.get_type_from_value(node.value)
            if self.is_known_global(tgt_id):
                scoped_target = tgt_id
            else:
                scoped_target = self.scoped_sym(tgt_id)
            if scoped_target not in self.types:     # First time we see this, so store it
                self.add_scoped_symbol_type(scoped_target, tgt_ty)
                self.add_symbol_to_scope(scoped_target)
            known_type = self.types[scoped_target]
            assert known_type == tgt_ty

    def visit_FunctionDef(self, node):
        func_name = node.name
        # Register this function
        self.add_scoped_symbol_type(func_name, 'func')

        self.enter_scope(func_name)
        self.generic_visit(node)    # visit all children of this node
        self.exit_scope(func_name)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if visitor == self.generic_visit:
            print(f"Would call {method} {node!r}")
        return visitor(node)

    def report(self):
        pprint(self.types)
        pprint(self.symbols)
