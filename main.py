import serial
import time
import serial.tools.list_ports

looping = 'y'
try:
    ser = serial.Serial('COM7', 115200, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()
  

def receiveData():
    print("Receiving Data")
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8').strip()
            print(f"Received from ESP32: {message}")


def checkPorts():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        print("Available ports:")
        for port in ports:
            print(port)
    else:
        print("No serial ports found.")

def sendData():
    # Entering data for user
    user_input = input("Enter data: ")

    try:
        byte_written = ser.write(user_input.encode()) 

        if byte_written > 0:
            print(f"Successfully sent {byte_written} bytes: {user_input}")
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error while sending data: {e}")
    

while looping == 'y' or looping == 'Y':
    sendData()
    looping = input("Do you want to send another? [Y/N] ") 

ser.close() 
