import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the relay
relay_pin = 17
GPIO.setup(relay_pin, GPIO.OUT)

def turn_off_current():
    # Turn off the relay (open the circuit)
    GPIO.output(relay_pin, GPIO.HIGH)

def turn_on_current():
    # Turn on the relay (close the circuit)
    GPIO.output(relay_pin, GPIO.LOW)

# Example: Turn off the current for 5 seconds
turn_off_current()
time.sleep(5)
turn_on_current()

# Clean up GPIO settings
GPIO.cleanup()