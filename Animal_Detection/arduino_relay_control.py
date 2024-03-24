import serial
import time

# Replace 'COM8' with the serial port connected to your Arduino
ser = serial.Serial('COM8', 9600, timeout=1)

def turn_relay_on():
    ser.write(b'1')  # Send '1' to turn on the relay
    print("Relay turned ON")

def turn_relay_off():
    ser.write(b'0')  # Send '0' to turn off the relay
    print("Relay turned OFF")

# Accept user input
while True:
    user_input = input("Enter '1' to turn on the relay, '0' to turn off, or 'q' to quit: ")

    if user_input == '1':
        turn_relay_on()
    elif user_input == '0':
        turn_relay_off()
    elif user_input == 'q':
        break
    else:
        print("Invalid input. Please enter '1', '0', or 'q'.")

# Close the serial connection when done
ser.close()
