from tests.test_ut import run_test_from_text, pos_test, neg_test


def test_simple_binop():
    pos_test(
        """
a=5
b=6
c=a+b
""",
        """int a;
int b;
int c;

a = 5;
b = 6;
c = (a + b);
""",
    )


def test_power_op():
    neg_test('''a=5**2''', "In line 1: [5] Unsupported binary operator")


def test_modulo():
    pos_test('''a=37 % 7''', '''int a;\n\na = (37 % 7);''')


orandxor_py = '''a=37|5
b=37&5
c=37^5
'''

orandxor_c = '''int a;
int b;
int c;

a = (37 | 5);
b = (37 & 5);
c = (37 ^ 5);
'''


def test_orandxor():
    pos_test(orandxor_py, orandxor_c)


def test_ifelse_expr():
    pos_test('''b=4
a=5 if b == 4 else 3''', '''int b;
int a;

b = 4;
a = ((b == 4) ? 5 : 3);''')


def test_ifelse_expr_diff_types():
    neg_test('''b=4
a=5 if b == 4 else "3"''', '''In line 2: [a=5 if b == 4 else "3"] Using if-expressions can only support same types''')


def test_shift_expr():
    pos_test('''a = (1 << 3) + (8 << 1)''', '''int a;

a = ((1 << 3) + (8 << 1));''')
