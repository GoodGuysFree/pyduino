
void setup() {
    /* Main Code */
    Serial.begin(9600);
}



void loop() {
    /* Local Variable Declarations */
    int sensorValue;

    /* Main Code */
    analogRead(A0);
    sensorValue = None;
    Serial.println(sensorValue);
    delay(1);
}


