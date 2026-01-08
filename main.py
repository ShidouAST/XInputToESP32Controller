import serial
import time
import serial.tools.list_ports
import pygame

looping = 'y'

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

def sendData(data):
    # Entering data for user
    # user_input = input("Enter data: ")
    try:
        byte_written = ser.write(f"{data}\n".encode()) 
        if byte_written > 0:
            print(f"Successfully sent {byte_written} bytes: {data}")
        else:
            print("Failed to send data.")
    except Exception as e:
        print(f"Error while sending data: {e}")

def controllerCheck():
    pygame.init()
    pygame.joystick.init()
    # Checking for available controllers
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("Controller Found")
    else:
        # Choose from the list
        joysticks = [pygame.joystick.Joystick(x) for x in range(joystick_count)]
        print("Lists of Controllers:")
        count = 0

        for joystick in joysticks:
            joystick.init()
            print(f"{count} - {joystick.get_name()}")
            count += 1
        chosenJoystick = input("Choose your controller(#): ")
        joystick = pygame.joystick.Joystick(int(chosenJoystick))

controllerCheck()
checkPorts()

port = input("Which Port to use (All Caps): ")

try:
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

running = True
print("Test the controller")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Button Presses
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} Pressed!")
            sendData(event.button)
        
        if event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.5: # deadzone
                print(f"Axis {event.axis} moved to {event.value:.2f}")
                sendData(f"{event.axis}/{event.value:.2f}")

pygame.quit()


# while looping == 'y' or looping == 'Y':
#     sendData()
#     looping = input("Do you want to send another? [Y/N] ") 

ser.close() 
