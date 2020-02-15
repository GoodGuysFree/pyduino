from tests.test_ut import pos_test, neg_test


test1_py = '''def myfunc(a: int) -> int:
    return a+5
'''

test1_c = '''int myfunc(int a);


int myfunc(int a) {
    return ((a + 5));
}'''


def test_forward_decl():
    pos_test(test1_py, test1_c)
