int amit;
int omri;

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



void loop() {
    delay(1000);
    Serial.println("Ahem...");
}


