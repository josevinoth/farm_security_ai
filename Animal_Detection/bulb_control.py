import requests

# Replace with the IP address or hostname of your NodeMCU
nodeMCU_ip = "192.168.1.23"
relay_endpoint = "/deactivate_relay"  # Change this endpoint based on your NodeMCU code

# Function to send a signal to control the relay
def control_relay(relay_endpoint):
    try:
        # Send an HTTP GET request to control the relay
        requests.get(f"http://{nodeMCU_ip}{relay_endpoint}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        while True:
            user_input = input("Enter 1 to activate relay, 0 to deactivate, or any other key to exit: ")

            if user_input.isdigit():  # Check if the input is a digit
                value = int(user_input)
                if value ==0:
                    relay_endpoint = "/deactivate_relay"
                    control_relay(relay_endpoint)
                elif value==1:
                    relay_endpoint = "/activate_relay"
                    control_relay(relay_endpoint)
                else:
                    print("Invalid input. Please enter 1 to activate or 0 to deactivate.")
            else:
                print("Exiting the script.")
                break

    except KeyboardInterrupt:
        print("Script terminated by user.")
