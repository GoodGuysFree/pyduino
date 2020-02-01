from tests.test_ut import pos_test, neg_test


def test_create_dict():
    pos_test('a = { 3: 4, }', '''dict_t a;

a = ({
    dict_t ret = ht_create(DEFAULT_DICT_SIZE);
    ht_put(ret, ((void*)(3)), ((void*)(4)));
    ret;
    });
''')
