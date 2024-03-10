import requests

nodeMCU_ip = "192.168.1.100"  # Replace with the NodeMCU's IP address

def turn_on_relay1():
    response = requests.get(f"http://{nodeMCU_ip}/turnonrelay1")
    print(response.text)

def turn_off_relay1():
    response = requests.get(f"http://{nodeMCU_ip}/turnoffrelay1")
    print(response.text)

# Example: Turn ON relay 1
turn_on_relay1()
