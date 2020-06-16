import time
import serial

arduino = serial.Serial('/dev/ttyUSB0', 9600)

while 1:

    cantidad = input("Ingrese cantidad de mediciones entre 1 y 9: ")

    arduino.write(cantidad.encode())

    time.sleep(2)

    rawString = arduino.readline()
    print(rawString)

arduino.close()
