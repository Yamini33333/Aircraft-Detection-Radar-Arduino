const int trigPin1 = 9;
const int echoPin1 = 10;

const int trigPin2 = 11;
const int echoPin2 = 12;

long duration1;
long duration2;

float distance1;
float distance2;

float getDistance(int trigPin, int echoPin) {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return 0;
  }

  return duration * 0.0343 / 2;
}

void setup() {

  Serial.begin(9600);

  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void loop() {

  distance1 = getDistance(trigPin1, echoPin1);

  delay(50);

  distance2 = getDistance(trigPin2, echoPin2);

  // Send data to Python GUI
  Serial.print(distance1);
  Serial.print(",");
  Serial.println(distance2);

  delay(100);
}
