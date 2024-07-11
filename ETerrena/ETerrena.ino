#include <avr/wdt.h> // Librería para el perro guardián (Watchdog)
#include <SPI.h>
#include <SD.h>
#include <RF24.h>

RF24 radio(8, 7); // CE, CSN
const byte address[6] = "00001"; // Dirección de lectura del CANSAT

struct DataPacket {
  int16_t altitude = 0;
  int16_t pressure = 0;
  int16_t acceleration[3] = {0, 0, 0};
  int16_t temperature = 0;
};

File dataFile;

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando la estación terrena...");

  // Inicializar el perro guardián con un tiempo de espera de 2 segundos
  wdt_enable(WDTO_2S);

  // Inicializar el módulo de radio
  radio.begin();
  radio.openReadingPipe(1, address); // Dirección de lectura del CANSAT
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_250KBPS);
  radio.setChannel(50);
  radio.startListening();

  // if (!SD.begin(4)) {
  //   Serial.println("error al iniciar la tarjeta SD");
  //   while (1);
  // }

  // dataFile = SD.open("DATA.csv", FILE_WRITE);
  // if (!dataFile) {
  //   Serial.println("Error al abrir el archivo DATA.csv");
  //   while (1);
  // }

  dataFile.println("Altitud (m),Presión (hPa),Aceleración X (m/s^2),Aceleración Y (m/s^2),Aceleración Z (m/s^2),Temperatura (°C)");
  dataFile.close();

  Serial.println("Estación terrena lista para recibir datos del CANSAT.");
}

void loop() {
  // Reiniciar el perro guardián para evitar que se reinicie el microcontrolador
  // mientras el código está funcionando correctamente
  wdt_reset();

  // Esperar hasta que se detecte el CANSAT encendido
  while (!radio.available()) {
    delay(1000);
    Serial.println("Esperando la señal del CANSAT...");
  }

  // Si hay datos disponibles del CANSAT, leerlos
  if (radio.available()) {
    DataPacket packet;
    radio.read(&packet, sizeof(packet));

    Serial.println("Datos recibidos del CANSAT:");

    Serial.print(packet.altitude);
    Serial.print(",");

    Serial.print(packet.pressure);
    Serial.print(",");

    Serial.print(packet.acceleration[0]);
    Serial.print(",");

    Serial.print(packet.acceleration[1]);
    Serial.print(",");

    Serial.print(packet.acceleration[2]);
    Serial.print(",");

    Serial.print(packet.temperature);
    Serial.println();

    //Guardar datos en la tarjeta SD
  //   dataFile = SD.open("DATA.csv", FILE_WRITE);
  //   if (dataFile) {
  //     dataFile.print(packet.altitude);
  //     dataFile.print(",");
  //     dataFile.print(packet.pressure);
  //     dataFile.print(",");
  //     dataFile.print(packet.acceleration[0]);
  //     dataFile.print(",");
  //     dataFile.print(packet.acceleration[1]);
  //     dataFile.print(",");
  //     dataFile.print(packet.acceleration[2]);
  //     dataFile.print(",");
  //     dataFile.print(packet.temperature);
  //     dataFile.println();
  //     dataFile.close();
  //     Serial.println("Datos guardados en la tarjeta SD.");
  //   } else {
  //     Serial.println("Error al abrir el archivo para escribir datos en la tarjeta SD");
  //   }
 }
}
