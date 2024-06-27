#include <avr/wdt.h> // Librería para el perro guardián (Watchdog)
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Adafruit_MPL3115A2.h>
#include <Adafruit_ADXL345_U.h>


RF24 radio(8, 7); // CE, CSN
Adafruit_MPL3115A2 mpl;
Adafruit_ADXL345_Unified accel;
const byte address[6] = "00001";

struct DataPacket {
 int16_t altitude;
 int16_t pressure;
 int16_t acceleration[3];
 int16_t temperature;
};

void setup() {
 Serial.begin(9600); // Inicializar la comunicación serial para depuración
 Serial.println("Iniciando...");

 // Inicializar el perro guardián con un tiempo de espera de 2 segundos
 wdt_enable(WDTO_2S);

 // Inicializar el módulo de radio
 radio.begin();
 radio.openWritingPipe(address);
 radio.setPALevel(RF24_PA_LOW);
 radio.setDataRate(RF24_250KBPS);
 radio.setChannel(50);
 radio.stopListening();

 if (!radio.isChipConnected()) {
   Serial.println("Error al inicializar el módulo de radio nRF24L01");
   while (1); // Detener el programa en caso de error
 }

 // Inicializar el sensor MPL3115A2
 if (!mpl.begin()) {
   Serial.println("Error al iniciar el sensor MPL3115A2");
   while (1); // Detener el programa en caso de error
 }

 // Inicializar el sensor ADXL345
 if (!accel.begin()) {
   Serial.println("Error al iniciar el sensor ADXL345");
   while (1); // Detener el programa en caso de error
 }

 accel.setRange(ADXL345_RANGE_2_G);
 Serial.println("Sensores inicializados correctamente.");
}

void loop() {
 // Reiniciar el perro guardián para evitar que se reinicie el microcontrolador
 // mientras el código está funcionando correctamente
 wdt_reset();

 sensors_event_t event;
 accel.getEvent(&event);
 int16_t altitude = mpl.getAltitude();
 int16_t pressure = mpl.getPressure() / 100;
 int16_t temperature = getTemperature();

 DataPacket packet;
 packet.altitude = altitude;
 packet.pressure = pressure;
 packet.acceleration[0] = event.acceleration.x;
 packet.acceleration[1] = event.acceleration.y;
 packet.acceleration[2] = event.acceleration.z;
 packet.temperature = temperature;

 radio.write(&packet, sizeof(packet));

 // Para depuración, imprimir los valores enviados
 Serial.print("Altitud: ");
 Serial.print(packet.altitude);
 Serial.println(" metros");

 Serial.print("Presión: ");
 Serial.print(packet.pressure);
 Serial.println(" hPa");

 Serial.print("Aceleración X: ");
 Serial.print(packet.acceleration[0]);
 Serial.println(" m/s^2");

 Serial.print("Aceleración Y: ");
 Serial.print(packet.acceleration[1]);
 Serial.println(" m/s^2");

 Serial.print("Aceleración Z: ");
 Serial.print(packet.acceleration[2]);
 Serial.println(" m/s^2");

 Serial.print("Temperatura: ");
 Serial.print(packet.temperature);
 Serial.println(" grados Celsius");
}

int16_t getTemperature() {
 int sensorValue = analogRead(A0);
 float voltage = sensorValue * (2.9 / 1023.0); // Considerar la referencia de voltaje de 3V
 return (int16_t)((voltage - 0.5) * 100.0);
}
