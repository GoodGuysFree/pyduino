void no_ret_annotation_no_ret(void);
int int_ret_annotation_int_ret(void);
double float_ret_annotation_float_ret(void);
int no_ret_annotation_1_int_ret(void);
void no_ret_annotation_ret_wo_val(void);
double no_ret_annotation_complex_ret(void);


void no_ret_annotation_no_ret(void) {
    print(1);
}



int int_ret_annotation_int_ret(void) {
    return (6);
}



double float_ret_annotation_float_ret(void) {
    return (3.14159265835);
}



int no_ret_annotation_1_int_ret(void) {
    int a;

    a = 76;
    return ((a / 2));
}



void no_ret_annotation_ret_wo_val(void) {
    print("Something");
    return;
}



double no_ret_annotation_complex_ret(void) {
    double a;
    double b;

    a = 8;
    b = 9;
    return ((a + b));
}


