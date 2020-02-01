from tests.test_ut import run_test_from_text, pos_test


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
