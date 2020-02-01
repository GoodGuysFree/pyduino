import ast


class PytocNodeVisitor(ast.NodeVisitor):
    def __init__(self, lines):
        self.lines = lines
        self.current_node = None

    def exception_msg(self, text, node=None):
        if node is None:
            node = self.current_node
        msg = f"In line {node.lineno}: ["
        src_lines = self.lines[node.lineno - 1 : node.end_lineno]
        src_lines[-1] = src_lines[-1][: node.end_col_offset]
        src_lines[0] = src_lines[0][node.col_offset :]
        src_text = " ".join(src_lines)
        msg += src_text
        msg += "] " + text
        return msg
