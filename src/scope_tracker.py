import ast


class ScopeTracker(ast.NodeVisitor):
    def __init__(self):
        self.curr_scope = []

    def current_scope(self):
        scope_string = ""
        if len(self.curr_scope) > 0:
            scope_string = "::".join(self.curr_scope)
        return scope_string

    def scoped_sym(self, symbol):
        if symbol.find("::") >= 0:
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
