from tests.test_ut import pos_test, neg_test


def test_simple_list():
    pos_test('''a = [ 3, 4, 5 ]''', '''int a[3] = { 3, 4, 5 };''')


def test_float_list():
    pos_test('''a = [ 1.0, 4.1, 2.2 ]''', '''double a[3] = { 1.0, 4.1, 2.2 };''')


def test_string_list():
    pos_test('a = [ "amit", "margalit" ]', 'String a[2] = { "amit", "margalit" };')
