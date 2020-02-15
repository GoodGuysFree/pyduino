int amit;
int omri;
void setup(int a, int b);
void loop(void);

amit = 8;
omri = 3;
amit = omri = 5;

void setup(int a, int b) {
    int c;

    c = 8;
    amit = 9;
    myfunc((b + (a / c)));
    Serial.begin((amit * 1200));
    pinMode(ledPin, OUTPUT);
}



void loop(void) {
    delay(1000);
    Serial.println("Ahem...");
}


