from tests.test_ut import pos_test, neg_test


def test_simple_declaration():
    pos_test("a = ''", 'string a;\n\na = "";')


def test_annotated_declaration():
    pos_test("a : str = ''", 'string a;\n\na = "";')


def test_assign_value():
    pos_test("a = 'foo'\na = 'bar'", 'string a;\n\na = "foo";\na = "bar";\n')
