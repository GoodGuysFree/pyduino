int amit;
int omri;

amit = 8;
omri = 3;
amit = omri = 5;

int setup(int a, int b) {
    /* Local Variable Declarations */
    int a;
    int b;
    int c;

    /* Main Code */
    c = 8;
    amit = 9;
    myfunc((b + (a / c)));
    Serial.begin((amit * 1200));
    pinMode(ledPin, OUTPUT);
}



int loop() {
    /* Main Code */
    delay(1000);
    Serial.println("Ahem...");
}


