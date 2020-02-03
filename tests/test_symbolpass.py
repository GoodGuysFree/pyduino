from tests.test_ut import neg_test


# Negative tests for SymbolPass


def test_no_exception_else_clause():
    try:
        neg_test("a = 5", "nothing")
    except AssertionError:
        pass


def test_unsupported_data_type():
    neg_test(
        "map = str(3)",
        "In line 1: [str(3)] Cannot obtain type information from unexpected node of type <_ast.Call object at 0x",
    )


# def test_unsupported_dict():
#     neg_test("map = dict()", "foo")


def test_unhomogeneous_list():
    neg_test(
        "lst = [3, 4.5]",
        "In line 1: [[3, 4.5]] Only homogeneous lists and tuples are supported.",
    )


def test_unhomogeneous_tuple():
    neg_test(
        "tup = (2.4, 5)",
        "In line 1: [(2.4, 5)] Only homogeneous lists and tuples are supported.",
    )


def test_empty_list():
    neg_test("empty = []", "In line 1: [[]] Empty lists not supported yet")


def test_same_type_on_binop():
    neg_test(
        "val = 3.3 + 5",
        "In line 1: [3.3 + 5] We do not support different types on binary operators.",
    )


def test_dual_annotation_diff_type():
    neg_test(
        """
var : int = 0
var : float = 4.4
""",
        "In line 3: [var : float = 4.4] Variable var annotated as being of type float but it is already known as being of type int",
    )


def test_dual_annotation_same_type():
    neg_test(
        """
var : int = 0
var : int = 4
""",
        "In line 3: [var : int = 4] Variable var is already known in scope",
    )
