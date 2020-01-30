ledPin  =  13 #;      // the number of the LED pin

amit = 8

def setup(a: int, b: int):
  c : int = 8

  global amit

  amit = 9

  myfunc(b + a/c)
  #// put your setup code here, to run once:
  Serial.begin(amit * 1200)

  #// initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT)


def loop():
  #// put your main code here, to run repeatedly:
  delay(1000)
  Serial.println("Ahem...")
