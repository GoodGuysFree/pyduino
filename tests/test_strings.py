from tests.test_ut import pos_test, neg_test


def test_simple_declaration():
    pos_test("a = ''", 'string a;\n\na = string("");')


def test_annotated_declaration():
    pos_test("a : str = ''", 'string a;\n\na = string("");')


def test_assign_value():
    pos_test(
        "a = 'foo'\na = 'bar'", 'string a;\n\na = string("foo");\na = string("bar");\n'
    )


def test_assign_wrong_type():
    neg_test(
        "a = 'foo'\na = 6",
        expected_message="In line 2: [a = 6] Assignment to a new different type is not supported.",
    )


def test_assign_plus_op():
    pos_test(
        code='a = "amit" + " margalit"',
        expected_output='string a;\n\na = (string("amit") + string(" margalit"));\n',
    )


# Advanced string test
advanced_string_test_py = '''
global_string = "Amit Margalit"

def func(v1: str, v2: str) -> str:
    """Simple Docstring"""
    return v1 + " = " + v2

ret1 = global_string + func("foo", "bar")
ret2 = "Assign: " + func("foo" + global_string, ret1)
'''
advanced_string_test_c = """
string global_string;
string ret1;
string ret2;

global_string = string("Amit Margalit");

string func(string v1, string v2) {
    /* Simple Docstring */
    return (((v1 + " = ") + v2));
}


ret1 = (global_string + func(string("foo"), string("bar")));
ret2 = (string("Assign: ") + func((string("foo") + global_string), ret1));
"""


def test_advanced_strings():
    pos_test(advanced_string_test_py, advanced_string_test_c)


def test_str_builtin():
    pos_test("a = str(6)", 'string a;\n\na = string("6");')
