from tests.test_ut import pos_test, neg_test


def test_simple_string_assign():
    pos_test('a = "test"', 'sds a;\n\nsdsfree(a); a = sdsnew("test");')


def test_simple_annotated_string_assign():
    pos_test('a : str = "test"', 'sds a;\n\nsdsfree(a); a = sdsnew("test");')


string_plus_op_py = """a = "Amit"
b = a + " Margalit"
"""
string_plus_op_c = """sds a;
sds b;

sdsfree(a); a = sdsnew("Amit");
sdsfree(b); b = sdscat(a, " Margalit");
"""


def test_string_operator_plus():
    pos_test(string_plus_op_py, string_plus_op_c)

