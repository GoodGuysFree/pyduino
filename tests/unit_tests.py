import ast
import io
import pytest
from generate_pass import GeneratePass
from symbol_pass import SymbolPass

test_files = [
    "test.py",
    "test_global.py",
    "test_unary_op.py",
    "test_arrays.py",
    "test_tuples.py",
    "test_func_retval.py",
    "test_sketch1.py",
]


def get_expect_filename(filename):
    base_name = filename.split(".")[0]
    return f"{base_name}-expect.c"


# Rename this to test_ to force re-gen (use with care)


def generate_expected_file(srcfile, expfile):
    exp_f = open(expfile, "w")
    text = open(srcfile).read()
    lines = text.splitlines()
    tree = ast.parse(text)
    symbols = SymbolPass(tree, lines)
    out_file = io.StringIO("")
    GeneratePass(symbols, tree, out_file, lines)
    out_file.seek(0, io.SEEK_SET)
    out_text = out_file.read()
    exp_f.write(out_text)
    exp_f.close()
    return out_text


def un_test_generate_expect_files():
    for test in test_files:
        exp_fn = get_expect_filename(test)
        generate_expected_file(test, exp_fn)


def test_all_files():
    for test in test_files:
        exp_file = get_expect_filename(test)
        try:
            exp_text = open(exp_file).read()
        except IOError:
            exp_text = generate_expected_file(test, exp_file)
        # Now generate the thing...
        out_file = io.StringIO("")
        text = open(test).read()
        lines = text.splitlines()
        tree = ast.parse(text)
        symbols = SymbolPass(tree, lines)
        GeneratePass(symbols, tree, out_file, lines)
        # Now get the string to compare...
        out_file.seek(0, io.SEEK_SET)
        out_text = out_file.read()
        if out_text != exp_text:
            with open(f"exp-{exp_file}", "w") as f:
                f.write(exp_text)
            with open(f"out-{exp_file}", "w") as f:
                f.write(out_text)
        assert out_text == exp_text
