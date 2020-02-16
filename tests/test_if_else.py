from tests.test_ut import pos_test, neg_test

test1_py = """a = 5
def setup():
    if a > 4:
        print("a is larger than 4")
"""
test1_c = """int a;
void setup(void);

a = 5;

void setup(void) {
    if (a > 4) {
        print("a is larger than 4");
    }
}"""


def test_simple_if_stmt():
    pos_test(test1_py, test1_c)


test2_py = """a = 5
def setup():
    if a > 4:
        print("a is larger than 4")
    else:
        print("a not larger than 4")
"""
test2_c = """int a;
void setup(void);

a = 5;

void setup(void) {
    if (a > 4) {
        print("a is larger than 4");
    } else {
        print("a not larger than 4");
    }
}
"""


def test_if_else_stmt():
    pos_test(test2_py, test2_c)


test3_py = """a = 5
def setup():
    if a > 4:
        print("a is larger than 4")
    elif a < 2:
        print("a less than 2")
"""
test3_c = """int a;
void setup(void);

a = 5;

void setup(void) {
    if (a > 4) {
        print("a is larger than 4");
    } else if (a < 2) {
        print("a less than 2");
    }
}"""


def test_if_elif_stmt():
    pos_test(test3_py, test3_c)


test4_py = """a = 5
def setup():
    if a > 4:
        print("a is larger than 4")
    elif a < 2:
        print("a less than 2")
    elif a < 0:
        exit(1)
"""
test4_c = """int a;
void setup(void);

a = 5;

void setup(void) {
    if (a > 4) {
        print("a is larger than 4");
    } else if (a < 2) {
        print("a less than 2");
    } else if (a < 0) {
        exit(1);
    }
}"""


def test_if_elif_elif_stmt():
    pos_test(test4_py, test4_c)


test5_py = """def testfunc():
    a = 5
    if a > 4:
        print("a is larger than 4")
    elif a < 2:
        print("a less than 2")
    elif a < 0:
        exit(1)
    else:
        exit(0)
"""
test5_c = """void testfunc(void);


void testfunc(void) {
    int a;

    a = 5;
    if (a > 4) {
        print("a is larger than 4");
    } else if (a < 2) {
        print("a less than 2");
    } else if (a < 0) {
        exit(1);
    } else {
        exit(0);
    }
}
"""


def test_if_elif_elif_else_stmt():
    pos_test(test5_py, test5_c)
