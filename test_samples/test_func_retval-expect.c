
void no_ret_annotation_no_ret() {
    /* Main Code */
    print(1);
}



int int_ret_annotation_int_ret() {
    /* Main Code */
    return (6);
}



float float_ret_annotation_float_ret() {
    /* Main Code */
    return (3.14159265835);
}



int no_ret_annotation_1_int_ret() {
    /* Local Variable Declarations */
    int a;

    /* Main Code */
    a = 76;
    return ((a / 2));
}



void no_ret_annotation_ret_wo_val() {
    /* Main Code */
    print("Something");
    return;
}



float no_ret_annotation_complex_ret() {
    /* Local Variable Declarations */
    float a;
    float b;

    /* Main Code */
    a = 8;
    b = 9;
    return ((a + b));
}


