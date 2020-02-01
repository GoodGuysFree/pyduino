g_var1 = 4
g_var2: int = 5


def test():
    global g_var1
    print(g_var1)
    print(g_var2)
    g_var1 = 3
    g_var2 = 2
