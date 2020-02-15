int g_var1;
int g_var2;
void test(void);

g_var1 = 4;
g_var2 = 5;

void test(void) {
    int g_var2;

    print(g_var1);
    print(g_var2);
    g_var1 = 3;
    g_var2 = 2;
}


