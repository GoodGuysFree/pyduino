from tests.test_ut import pos_test, neg_test


test1_py = '''def looptest():
    for x in [1,2,3]:
        print(x)
'''

test1_c = '''void looptest(void);


void looptest(void) {
    int x;

    {
        int _temp_array[3] = { 1, 2, 3, };
        int _temp_index;
        for (_temp_index = 0; _temp_index < 3; _temp_index++) {
            x = _temp_array[_temp_index];
            print(x);
        }
    }
}'''


def test_loop_literal_list():
    pos_test(test1_py, test1_c)


test2_py = '''def looptest():
    for x in ['foo', 'bar', '3']:
        print(x)
'''

test2_c = '''void looptest(void);


void looptest(void) {
    String x;

    {
        String _temp_array[3] = { String("foo"), String("bar"), String("3"), };
        int _temp_index;
        for (_temp_index = 0; _temp_index < 3; _temp_index++) {
            x = _temp_array[_temp_index];
            print(x);
        }
    }
}
'''


def test_loop_string_list():
    pos_test(test2_py, test2_c)

