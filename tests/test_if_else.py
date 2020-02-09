from tests.test_ut import pos_test, neg_test

test1_py = """a = 5
if a > 4:
    print("a is larger than 4")
"""
test1_c = """int a;

a = 5;
if (a > 4) {
    print("a is larger than 4");
}
"""


def test_simple_if_stmt():
    pos_test(test1_py, test1_c)
