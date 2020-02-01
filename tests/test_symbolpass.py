from tests.test_ut import run_test_from_text


# Negative tests for SymbolPass


def test_strings_not_supported():
    try:
        run_test_from_text('''str_var = "test"''')
    except Exception as e:
        assert str(e) == 'In line 1: ["test"] Strings not yet supported'


def test_unsupported_data_type():
    try:
        run_test_from_text("""map = {1: 3,}""")
    except Exception as e:
        assert str(e).startswith(
            "In line 1: [{1: 3,}] Cannot obtain type information from unexpected node of type <_ast.Dict object at 0x"
        )

def test_unhomogeneous_list():
    try:
        run_test_from_text('''lst = [3, 4.5]''')
    except Exception as e:
        assert str(e) == 'In line 1: [[3, 4.5]] Only homogeneous lists and tuples are supported.'

def test_unhomogeneous_tuple():
    try:
        run_test_from_text('''tup = (2.4, 5)''')
    except Exception as e:
        assert str(e) == 'In line 1: [(2.4, 5)] Only homogeneous lists and tuples are supported.'
