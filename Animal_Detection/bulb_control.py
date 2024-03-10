import requests

# Replace with your NodeMCU's IP address and port
nodemcu_ip = "192.168.1.100"
nodemcu_port = 80

# Function to control the relay
def control_relay(input_value):
    url = f"http://{nodemcu_ip}:{nodemcu_port}/control?input={input_value}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Relay control successful. Input: {input_value}")
        else:
            print(f"Failed to control relay. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Take user input for relay control
while True:
    user_input = input("Enter 1 to switch on, 0 to switch off, or q to quit: ")

    if user_input.lower() == 'q':
        break

    try:
        input_value = int(user_input)
        if input_value == 0 or input_value == 1:
            control_relay(input_value)
        else:
            print("Invalid input. Please enter 0 to switch off or 1 to switch on.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
