ledPin  =  13 #;      // the number of the LED pin


def setup(a: int, b: int):
  myfunc(3+2)
  #// put your setup code here, to run once:
  Serial.begin(9600)

  #// initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT)


def loop():
  #// put your main code here, to run repeatedly:
  delay(1000)
  Serial.println("Ahem...")
