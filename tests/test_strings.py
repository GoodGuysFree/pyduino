from tests.test_ut import pos_test, neg_test


def test_simple_declaration():
    pos_test("a = ''", 'String a;\n\na = String("");')


def test_annotated_declaration():
    pos_test("a : str = ''", 'String a;\n\na = String("");')


def test_assign_value():
    pos_test(
        "a = 'foo'\na = 'bar'", 'String a;\n\na = String("foo");\na = String("bar");\n'
    )


def test_assign_wrong_type():
    neg_test(
        "a = 'foo'\na = 6",
        expected_message="In line 2: [a = 6] Assignment to a new different type is not supported.",
    )


def test_assign_plus_op():
    pos_test(
        code='a = "amit" + " margalit"',
        expected_output='String a;\n\na = (String("amit") + String(" margalit"));\n',
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
String global_string;
String func(String v1, String v2);
String ret1;
String ret2;

global_string = String("Amit Margalit");

String func(String v1, String v2) {
    /* Simple Docstring */
    return (((v1 + " = ") + v2));
}


ret1 = (global_string + func(String("foo"), String("bar")));
ret2 = (String("Assign: ") + func((String("foo") + global_string), ret1));
"""


def test_advanced_strings():
    pos_test(advanced_string_test_py, advanced_string_test_c)


def test_str_builtin():
    pos_test("a = str(6)", 'String a;\n\na = String("6");')


def test_string_slices():
    pos_test('''a = "amit margalit"
b = a[2:-3]
c = 1
b = a[c:6]''', '''String a;
String b;
int c;

a = String("amit margalit");
b = a.substr(2, (a.size()-3-2));
c = 1;
b = a.substr(c, (6-c));
''')

def test_advanced_slice1():
    pos_test('''a = "amit margalit"
b = a[1:2]
i = 4;
b = a[i:i+1]''','''String a;
String b;
int i;

a = String("amit margalit");
b = a.substr(1, (2-1));
i = 4;
b = a.substr(i, ((i + 1)-i));''')
