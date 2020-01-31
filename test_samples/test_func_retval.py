# Test function return values


def no_ret_annotation_no_ret():
    print(1)


def int_ret_annotation_int_ret() -> int:
    return 6


def float_ret_annotation_float_ret() -> float:
    return 3.14159265835


def no_ret_annotation_1_int_ret():
    a : int = 76
    return a / 2


def no_ret_annotation_ret_wo_val():
    print("Something")
    return


def no_ret_annotation_complex_ret():
    a : float = 8
    b : float = 9
    return a + b
