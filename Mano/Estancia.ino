#include <Servo.h>  // Librería para controlar servos

// Declarar los servos
Servo dedo1;
Servo dedo2;
Servo dedo3;
Servo dedo4;
Servo pulgar;

// Variables para almacenar los ángulos recibidos
int angulo1 = 0;
int angulo2 = 0;
int angulo3 = 0;
int angulo4 = 0;
int anguloPulgar = 0;

void setup() {
  // Inicializar comunicación serial
  Serial.begin(9600);

  // Asociar los servos a los pines
  dedo1.attach(3);  // Servo en pin D3
  dedo2.attach(5);  // Servo en pin D5
  dedo3.attach(6);  // Servo en pin D6
  dedo4.attach(9);  // Servo en pin D9
  pulgar.attach(10); // Servo en pin D10
}

void loop() {
  // Verificar si se ha recibido algún dato por el puerto serial
  if (Serial.available() > 0) {
    // Leer la información serial (ángulos para cada servo)
    angulo1 = Serial.parseInt();
    angulo2 = Serial.parseInt();
    angulo3 = Serial.parseInt();
    angulo4 = Serial.parseInt();
    anguloPulgar = Serial.parseInt();

    // Mover los servos según los ángulos recibidos
    dedo1.write(angulo1);
    dedo2.write(angulo2);
    dedo3.write(angulo3);
    dedo4.write(angulo4);
    pulgar.write(anguloPulgar);

    // Esperar un breve tiempo para permitir que los servos se posicionen
    delay(15);
  }
}
