import ast
from pprint import pprint

# scoped-symbol:
# <func/class>::<symbol>
from scope_tracker import ScopeTracker


class SymbolPass(ScopeTracker):
    def __init__(self, tree):
        super().__init__()
        self.symbols = {}  # key = scope, value = set of scoped symbol-names in this scope
        self.types = {}    # key = scoped-symbol, value = python type
        self.visit(tree)

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
        elif isinstance(value_node, ast.UnaryOp):
            assert isinstance(value_node.op, ast.USub) or isinstance(value_node.op, ast.UAdd)
            return self.get_type_from_value(value_node.operand)
        elif isinstance(value_node, ast.Name):
            target = self.scoped_sym(value_node.id)
            return self.find_type(target)
        elif isinstance(value_node, ast.BinOp):
            l_type = self.get_type_from_value(value_node.left)
            r_type = self.get_type_from_value(value_node.right)
            assert l_type == r_type
            return l_type
        elif isinstance(value_node, ast.List) or isinstance(value_node, ast.Tuple):
            list_size = len(value_node.elts)
            if list_size == 0:
                raise Exception("We are unable to handle empty lists, yet")
            el0_type = self.get_type_from_value(value_node.elts[0])
            assert all([self.get_type_from_value(x) == el0_type for x in value_node.elts])
            return f"list:{list_size}:{el0_type}"
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

    def handle_annotated_variable(self, var_name, var_type):
        '''An annotated assignment is local by definition'''
        scoped_target = self.scoped_sym(var_name)
        known_type = self.types.get(scoped_target, var_type)
        assert known_type == var_type
        assert not self.is_known_in_scope(var_name)
        self.add_symbol_to_scope(scoped_target)
        self.add_scoped_symbol_type(scoped_target, var_type)

    def find_local_syms(self, scope):
        scope_syms = self.symbols.get(scope, set())
        return set([x for x in scope_syms if x.startswith(scope)])

    def find_type(self, symbol):
        if symbol in self.types:
            return self.types[symbol]
        elif self.unscoped_sym(symbol) in self.types:
            return self.types[self.unscoped_sym(symbol)]
        else:
            raise Exception(f"Trying to find type for {symbol=} but it cannot be found.")

    @staticmethod
    def unscoped_sym(symbol):
        if symbol.find('::') >= 0:
            parts = symbol.split('::')
            return parts[-1]
        else:
            return symbol

    def visit_Global(self, node):
        this_scope = self.current_scope()
        this_scope_symbols = self.symbols.get(this_scope, set())
        this_scope_symbols.update(node.names)
        self.symbols[this_scope] = this_scope_symbols

    def visit_AnnAssign(self, node):
        '''Assignment with annotation'''
        self.handle_annotated_variable(node.target.id, node.annotation.id)

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

    def visit_arg(self, node):
        arg_name = node.arg
        if node.annotation is not None:
            arg_type = node.annotation.id
            self.handle_annotated_variable(arg_name, arg_type)
        else:  # So we know the argument, but not its type... We'll store it as a symbol but not its type
            self.add_symbol_to_scope(self.scoped_sym(arg_name))

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        #if visitor == self.generic_visit:
        #    print(f"Would call {method} {node!r}")
        return visitor(node)

    def report(self):
        pprint(self.types)
        pprint(self.symbols)
