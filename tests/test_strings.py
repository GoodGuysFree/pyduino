from tests.test_ut import pos_test, neg_test


def test_simple_declaration():
    pos_test("a = ''", 'string a;\n\na = "";')


def test_annotated_declaration():
    pos_test("a : str = ''", 'string a;\n\na = "";')


def test_assign_value():
    pos_test("a = 'foo'\na = 'bar'", 'string a;\n\na = "foo";\na = "bar";\n')


def test_assign_wrong_type():
    neg_test(
        "a = 'foo'\na = 6",
        expected_message="In line 2: [a = 6] Assignment to a new different type is not supported.",
    )


def test_assign_plus_op():
    pos_test(
        code='a = "amit" + " margalit"',
        expected_output='string a;\n\na = ("amit" + " margalit");\n',
    )
