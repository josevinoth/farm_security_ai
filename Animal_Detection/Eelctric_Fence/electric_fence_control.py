import serial
import time

arduino_port = ""  # Replace with your actual COM port (e.g., COM3)
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Allow time for Arduino to reset

try:
    while True:
        user_input = input("Enter '1' to turn on the LED, '0' to turn it off: ")
        if user_input == '1' or user_input == '0':
            ser.write(user_input.encode())
            time.sleep(1)
        else:
            print("Invalid input. Enter '1' or '0'.")

except KeyboardInterrupt:
    print("Exiting the script")
    ser.close()