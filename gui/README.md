# Tuzo CanSat Monitor

## Guía de uso

### Usando paquetes provistos

1. **Descargar paquete correspondiente para su sistema operativo** Desde la sección de “Releases” en el [repositorio de GitHub](https://github.com/AyrXZ47/cansat1/releases).

2. **Ejecutar**

   - **Windows**  
     Dado que los binarios no están firmados, será necesario desactivar la protección del antivirus / Windows Defender. Al abrir el ejecutable descargado, se debe permitir la ejecución en el diálogo de SmartScreen.

   - **Mac**  
     Gatekeeper no permitirá la ejecución del programa, por lo que será necesario añadir una excepción. En la terminal, ejecutar el siguiente comando:
     ```sh
     xattr -d com.apple.quarantine <Ruta del bundle .app>
     ```

   - **Linux**  
     En algunas distribuciones de Linux, basta con dar doble click sobre el archivo descargado. Si no, se debe ejecutar desde la terminal como un script.
   
     Tanto en Mac como en Linux, si se quiere visualizar la consola mientras el programa está en ejecución, se deberá ejecutar como script desde la terminal.

### Usando desde código fuente

1. **Clonar repositorio en una carpeta local**
     ```
     git clone https://github.com/AyrXZ47/cansat1.git
     ```
2. **Crear un entorno virtual de Python**
    ```
    python3 -m venv venv
    ```
   
3. **Entrar al entorno virtual**

- **Windows:**
  ```
  venv\Scripts\activate
  ```

- **Mac OS / Linux:**
  ```
  source venv/bin/activate
  ```

4. **Instalar dependencias del archivo requirements.txt**
    ```
    pip install -r requirements.txt
    ```
5. **Ejecutar archivo main.py**
    ```
    python3 main.py
    ```

### Creando paquete propio

Seguir hasta el paso 4 de “Usando desde código fuente”

1. **Instalar pyinstaller dentro del entorno virtual**
    ```
    pip install pyinstaller
    ```
   
2. **Empaquetar**

- **Windows (con consola)**
  ```
  pyinstaller --onefile --icon=resources/icono.ico --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" --name cansat-monitor main.py
  ```

- **Windows (sin consola)**
  ```
  pyinstaller --onefile --windowed --icon=resources/icono.ico --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" --name cansat-monitor main.py
  ```

- **Mac**
  ```
  pyinstaller --onefile --windowed --icon=resources/icon.icns --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" main.py
  ```

- **Linux**
  ```
  pyinstaller --onefile --windowed --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" main.py
  ```

3. **Ejecutar archivo generado en dist/**


## Attributions

This project uses the following third-party assets:

- **Low Poly Soda Can** by sanekcloff, available at [ https://skfb.ly/owLss](https://skfb.ly/owLss) licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).