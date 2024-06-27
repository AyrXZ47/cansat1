from serial_communication.arduino_comm import ArduinoComm

arduino = ArduinoComm()
ports = arduino.list_available_ports()
for x in range(len(ports)):
    print(x+1, ports[x],)
port_number = int(input("Selecciona puerto "))
arduino.select_port(ports[port_number - 1].device.split()[0])
arduino.begin_communication()
arduino.msg_test()