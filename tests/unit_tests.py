import ast
import io
import pytest
from generate_pass import GeneratePass
from symbol_pass import SymbolPass

test_files = [
    'test.py',
    'test_global.py',
    'test_unary_op.py',
    'test_arrays.py',
]


def get_expect_filename(filename):
    base_name = filename.split('.')[0]
    return f"{base_name}-expect.c"


# Rename this to test_ to force re-gen (use with care)
def un_test_generate_expect_files():
    for test in test_files:
        exp_fn = get_expect_filename(test)
        exp_f = open(exp_fn, 'w')
        tree = ast.parse(open(test).read())
        symbols = SymbolPass(tree)
        GeneratePass(symbols, tree, exp_f)


def test_all_files():
    for test in test_files:
        exp_file = get_expect_filename(test)
        exp_text = open(exp_file).read()
        # Now generate the thing...
        out_file = io.StringIO("")
        tree = ast.parse(open(test).read())
        symbols = SymbolPass(tree)
        GeneratePass(symbols, tree, out_file)
        # Now get the string to compare...
        out_file.seek(0, io.SEEK_SET)
        out_text = out_file.read()
        if out_text != exp_text:
            with open(f"exp-{exp_file}", "w") as f:
                f.write(exp_text)
            with open(f"out-{exp_file}", "w") as f:
                f.write(out_text)
        assert out_text == exp_text

