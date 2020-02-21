from tests.test_ut import pos_test, neg_test

simple_bool_py = """
var : bool = True
"""

simple_bool_c = """bool var;

var = true;
"""


def test_boolean_assign():
    pos_test(simple_bool_py, simple_bool_c)


simple_bool_annotation_py = """def boolfunc(var1 : bool) -> bool:
    return False
"""

simple_bool_annotation_c = """bool boolfunc(bool var1);


bool boolfunc(bool var1) {
    return (false);
}


"""


def test_boolean_annotation():
    pos_test(simple_bool_annotation_py, simple_bool_annotation_c)


wrong_type_return_py = """def func() -> bool:
    return 6
"""
wrong_type_return_exception = "In line 2: [return 6] Function should return 'bool' but this return statement is of type 'int'"


def test_wrong_type_return():
    neg_test(wrong_type_return_py, wrong_type_return_exception)


boolean_op_result_assignment_py = """c : bool = 6 < 3
b = 4
a = 3
c = b < a
"""
boolean_op_result_assignment_c = """
bool c;
int b;
int a;

c = (6 < 3);
b = 4;
a = 3;
c = (b < a);
"""


def test_boolean_op_result_assignment():
    pos_test(boolean_op_result_assignment_py, boolean_op_result_assignment_c)


def test_boolean_and_or_assignment():
    pos_test("""a = (6 > 4) and ((5 == 4) or (4 <= 5))""", "bool a;\n\na = ((6 > 4) and ((5 == 4) or (4 <= 5)));")


def test_boolean_not_assignment():
    pos_test("a = not 6 > 4", "bool a;\n\na = !(6 > 4);")


def test_bool_lst_assignment():
    pos_test("a = [True, False]", "bool a[2] = { true, false };")
