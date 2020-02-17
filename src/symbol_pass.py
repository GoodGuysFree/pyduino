import ast

# scoped-symbol:
# <func/class>::<symbol>
from scope_tracker import ScopeTracker


class SymbolPass(ScopeTracker):
    builtin_typecall_names = ("tuple", "set", "list", "str")

    def __init__(self, tree, lines):
        super().__init__(lines)
        # self.symbols: dictionary with:
        #   key = scope
        #   value = array of scoped symbol-names in this scope
        self.symbols = {}
        self.types = {}  # key = scoped-symbol, value = python type
        self.func_args = (
            {}
        )  # key = scoped function symbol, value = scoped argument name
        self.lines = lines

        # Run the tree
        self.visit(tree)

    def validate_same_type(self, items, tag):
        if len(items) == 0:
            return None
        i0_type = self.get_type_from_value(items[0])
        if not all([self.get_type_from_value(item) == i0_type for item in items]):
            raise self.exception(f"All items of {tag} must be of the same type.")
        return i0_type

    def add_func_argument(self, arg_name):
        curr_scope = self.current_scope()
        arg_list = self.func_args.get(curr_scope, [])
        arg_list.append(self.scoped_sym(arg_name))
        self.func_args[curr_scope] = arg_list

    def get_type_from_constant(self, value_node):
        value = value_node.value
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, float):
            return "float"
        else:
            raise self.exception(
                f"Unsupported constant value type: {value}", node=value_node
            )  # TODO: how to test this???

    def get_type_from_unaryop(self, value_node):
        op = value_node.op
        if (
                isinstance(op, ast.USub)
                or isinstance(op, ast.UAdd)
                or isinstance(op, ast.Not)
        ):
            return self.get_type_from_value(value_node.operand)
        else:
            raise self.exception(
                "Only +/-/not unary operators are supported.", node=value_node
            )  # no way to test, afaik

    def get_type_from_binop(self, value_node):
        l_type = self.get_type_from_value(value_node.left)
        ltype = l_type if l_type.find(":") < 0 else l_type.split(":")[1]
        r_type = self.get_type_from_value(value_node.right)
        rtype = r_type if r_type.find(":") < 0 else r_type.split(":")[1]
        if ltype != rtype:
            raise self.exception(
                "We do not support different types on binary operators.",
                node=value_node,
            )  # tested
        return l_type

    def get_type_from_iterable(self, node, elem_list):
        list_size = len(elem_list)
        if list_size == 0:
            raise self.exception("Empty lists not supported yet", node=node)  # tested
        t_el0 = self.get_type_from_value(elem_list[0])
        same_as_el0 = [self.get_type_from_value(x) == t_el0 for x in elem_list]
        if not all(same_as_el0):
            raise self.exception(
                "Only homogeneous lists and tuples are supported.", node=node
            )  # tested
        return f"list:{list_size}:{t_el0}"

    def get_type_from_ifexpr(self, vnode):
        body_type = self.get_type_from_value(vnode.body)
        else_type = self.get_type_from_value(vnode.orelse)
        if body_type != else_type:
            raise self.exception("Using if-expressions can only support same types")
        return body_type

    def get_type_from_value(self, vnode):
        if isinstance(vnode, ast.Constant):
            return self.get_type_from_constant(vnode)
        elif isinstance(vnode, ast.UnaryOp):
            return self.get_type_from_unaryop(vnode)
        elif isinstance(vnode, ast.Compare) or isinstance(vnode, ast.BoolOp):
            return "bool"
        elif isinstance(vnode, str):
            return "str"
        elif isinstance(vnode, ast.Name):
            return self.find_type(self.scoped_sym(vnode.id))
        elif isinstance(vnode, ast.BinOp):
            return self.get_type_from_binop(vnode)
        elif isinstance(vnode, ast.List) or isinstance(vnode, ast.Tuple):
            return self.get_type_from_iterable(vnode, vnode.elts)
        elif isinstance(vnode, ast.Call) and vnode.func.id in ("list", "tuple",):
            return self.get_type_from_iterable(vnode, vnode.args)
        elif isinstance(vnode, ast.Call):
            if vnode.func.id in self.builtin_typecall_names:
                return self.get_type_from_builtin_typecall(vnode)
            return self.find_type(vnode.func.id)
        elif isinstance(vnode, ast.IfExp):
            return self.get_type_from_ifexpr(vnode)
        # If we got here - it's unhandled...
        raise self.exception(
            f"Cannot obtain type information from unexpected node of type {vnode}",
            node=vnode,
        )  # tested

    def get_type_from_builtin_typecall(self, value_node):
        builtin = value_node.func.id
        if builtin == "str":
            return "str"
        else:
            raise self.exception(f"Not implemented yet.")

    def add_symbol_to_scope(self, symbol, scope=None):
        if scope is None:
            this_scope = self.current_scope()
        else:
            this_scope = scope
        scope_symbols = self.symbols.get(this_scope, [])
        if symbol not in scope_symbols:
            scope_symbols.append(symbol)
        self.symbols[this_scope] = scope_symbols

    def is_known_in_scope(self, symbol, scope=None):
        if scope is None:
            this_scope = self.current_scope()
        else:
            this_scope = scope
        return symbol in self.symbols.get(this_scope, [])

    def is_known_global(self, symbol):
        return self.is_known_in_scope(symbol, self.current_scope())

    def add_scoped_symbol_type(self, s_name, s_type):
        scoped_sym = self.scoped_sym(s_name)
        if scoped_sym in self.types:
            raise self.exception(
                f"Symbol {s_name} already has a type associated with it,"
            )
        self.types[scoped_sym] = s_type

    def set_func_ret_type(self, symbol, new_type):
        if symbol not in self.types:
            raise self.exception(
                f"Trying to update function '{symbol}' return value type to '{new_type}' but function is not known"
            )
        known_type = self.types[symbol]
        if known_type != "func":
            raise self.exception(
                f"Trying to update function '{symbol}' return value type to '{new_type}' but function is already has '{known_type}'"
            )
        self.types[symbol] = f"func:{new_type}"

    def handle_annotated_variable(self, var_name, var_type):
        """An annotated assignment is local by definition"""
        scoped_target = self.scoped_sym(var_name)
        known_type = self.types.get(scoped_target, var_type)
        if known_type != var_type:
            raise self.exception(
                f"Variable {var_name} annotated as being of type {var_type} "
                f"but it is already known as being of type {known_type}",
            )
        if self.is_known_in_scope(var_name):
            raise self.exception(
                f"Variable {var_name} is already known in scope {self.current_scope()}",
            )
        self.add_symbol_to_scope(scoped_target)
        self.add_scoped_symbol_type(scoped_target, var_type)

    def find_local_syms(self, scope, include_function_args=True):
        scope_syms = self.symbols.get(scope, [])
        if not include_function_args:
            scope_syms = [
                x for x in scope_syms if x not in self.func_args.get(scope, set())
            ]
        return [x for x in scope_syms if x.startswith(scope)]

    def find_function_args(self, funcname):
        return self.func_args.get(funcname)

    def find_type(self, symbol, node=None):
        if symbol in self.types:
            return self.types[symbol]
        elif self.unscoped_sym(symbol) in self.types:
            return self.types[self.unscoped_sym(symbol)]
        else:
            raise self.exception(
                f"Trying to find type for {symbol=} but it cannot be found.", node=node
            )

    def find_ret_type(self, scoped_func_name, node=None):
        stored_type = self.find_type(scoped_func_name)
        if stored_type == "func":
            return "void"
        elif ":" in stored_type:
            parts = stored_type.split(":")
            assert len(parts) == 2
            assert parts[0] == "func"
            return parts[1]
        else:
            raise self.exception(
                f"Internal error trying to find ret type for {scoped_func_name}",
                node=node,
            )

    @staticmethod
    def unscoped_sym(symbol):
        if symbol.find("::") >= 0:
            parts = symbol.split("::")
            return parts[-1]
        else:
            return symbol

    #=== Visit functions from here ===#

    def visit_Global(self, node):
        this_scope = self.current_scope()
        this_scope_symbols = self.symbols.get(this_scope, [])
        for name in node.names:
            if name not in this_scope_symbols:
                this_scope_symbols.append(name)
        self.symbols[this_scope] = this_scope_symbols

    def visit_AnnAssign(self, node):
        """Assignment with annotation"""
        self.handle_annotated_variable(node.target.id, node.annotation.id)

    def visit_For(self, node):
        scoped_target_symbol = self.scoped_sym(node.target.id)
        if len(node.iter.elts) == 0:
            return
        scoped_target_type = self.get_type_from_value(node.iter.elts[0])
        self.validate_same_type(node.iter.elts, f"for {node.target.id} in ...")
        if scoped_target_symbol not in self.symbols:
            self.add_symbol_to_scope(scoped_target_symbol)
        if scoped_target_symbol not in self.types:
            self.add_scoped_symbol_type(scoped_target_symbol, scoped_target_type)

    def visit_Assign(self, node):
        """Assignment without annotation:
           Check if symbol is new or existing.
           If existing, try to check if the type is the same. In C we can't change types..."""
        for target in node.targets:
            tgt_id = target.id
            tgt_ty = self.get_type_from_value(node.value)
            if self.is_known_global(tgt_id):
                scoped_target = tgt_id
            else:
                scoped_target = self.scoped_sym(tgt_id)
            if scoped_target not in self.types:  # First time we see this, so store it
                self.add_scoped_symbol_type(scoped_target, tgt_ty)
                self.add_symbol_to_scope(scoped_target)
            known_type = self.types[scoped_target]
            if known_type != tgt_ty:
                raise self.exception(
                    f"Assignment to a new different type is not supported."
                    + f" {scoped_target} is of type {known_type} and is assigned a value of type {tgt_ty}"
                )

    def visit_FunctionDef(self, node):
        func_name = node.name

        # Register this function, first try to find return type
        if node.returns is not None:
            self.add_scoped_symbol_type(func_name, f"func:{node.returns.id}")
        else:
            self.add_scoped_symbol_type(
                func_name, "func",
            )  # In this case we will try in visit_Return
        self.add_symbol_to_scope(func_name)

        self.enter_scope(func_name)
        self.generic_visit(node)  # visit all children of this node
        self.exit_scope(func_name)

    def visit_Return(self, node):
        if node.value is None:
            type_of_this_return = "void"
        else:
            type_of_this_return = self.get_type_from_value(node.value)
        known_type = self.find_type(
            self.current_scope()
        )  # current scope is exactly our function...
        if known_type == "func":
            self.set_func_ret_type(self.current_scope(), type_of_this_return)
        else:
            if f"func:{type_of_this_return}" != known_type:
                show_known_type = known_type.split(":")[1]
                raise self.exception(
                    f"Function should return '{show_known_type}' "
                    f"but this return statement is of type '{type_of_this_return}'"
                )

    def visit_arg(self, node):
        arg_name = node.arg
        if node.annotation is not None:
            arg_type = node.annotation.id
            self.handle_annotated_variable(arg_name, arg_type)
        else:  # So we know the argument, but not its type... We'll store it as a symbol but not its type
            self.add_symbol_to_scope(self.scoped_sym(arg_name))
        self.add_func_argument(arg_name)

    def visit(self, node):
        """Visit a node."""
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        # if visitor == self.generic_visit:
        #    print(f"Would call {method} {node!r}")
        self.current_node = node  # will be used for easy error reporting
        return visitor(node)
