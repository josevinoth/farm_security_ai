import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import filedialog

import requests
import serial
from PIL import ImageTk, Image
from keras.models import load_model
import numpy as np
import cv2

# Load the trained model to classify Animals
model = load_model('C:/Users/Franciska Fdo/PycharmProjects/farm_security_ai_v1.0/model/full_model.h5')

# Dictionary to label all traffic signs class.
classes = {
    0: {'name': 'Bee', 'size': 'small'},
    1: {'name': 'Beetle', 'size': 'small'},
    2: {'name': 'Bison', 'size': 'large'},
    3: {'name': 'Boar', 'size': 'large'},
    4: {'name': 'Butterfly', 'size': 'small'},
    5: {'name': 'Cat', 'size': 'medium'},
    6: {'name': 'Caterpillar', 'size': 'small'},
    7: {'name': 'Chimpanzee', 'size': 'large'},
    8: {'name': 'Cockroach', 'size': 'small'},
    9: {'name': 'Cow', 'size': 'large'},
    10: {'name': 'Coyote', 'size': 'medium'},
    11: {'name': 'Crab', 'size': 'small'},
    12: {'name': 'Crow', 'size': 'small'},
    13: {'name': 'Deer', 'size': 'large'},
    14: {'name': 'Dog', 'size': 'medium'},
    15: {'name': 'Dolphin', 'size': 'large'},
    16: {'name': 'Donkey', 'size': 'large'},
    17: {'name': 'Dragonfly', 'size': 'small'},
    18: {'name': 'Duck', 'size': 'small'},
    19: {'name': 'Eagle', 'size': 'medium'},
    20: {'name': 'Elephant', 'size': 'large'},
    21: {'name': 'Fire', 'size': 'small'},  # Fire isn't an animal, you might want to reconsider this.
    22: {'name': 'Flamingo', 'size': 'medium'},
    23: {'name': 'Fly', 'size': 'small'},
    24: {'name': 'Fox', 'size': 'medium'},
    25: {'name': 'Goat', 'size': 'medium'},
    26: {'name': 'Goldfish', 'size': 'small'},
    27: {'name': 'Goose', 'size': 'small'},
    28: {'name': 'Gorilla', 'size': 'large'},
    29: {'name': 'Grasshopper', 'size': 'small'},
    30: {'name': 'Hamster', 'size': 'small'},
    31: {'name': 'Hare', 'size': 'small'},
    32: {'name': 'Hedgehog', 'size': 'small'},
    33: {'name': 'Hippopotamus', 'size': 'large'},
    34: {'name': 'Hornbill', 'size': 'medium'},
    35: {'name': 'Horse', 'size': 'large'},
    36: {'name': 'Human', 'size': 'small'},
    37: {'name': 'Hummingbird', 'size': 'small'},
    38: {'name': 'Hyena', 'size': 'medium'},
    39: {'name': 'Jellyfish', 'size': 'small'},
    40: {'name': 'Kangaroo', 'size': 'large'},
    41: {'name': 'Koala', 'size': 'small'},
    42: {'name': 'Ladybugs', 'size': 'small'},
    43: {'name': 'Leopard', 'size': 'large'},
    44: {'name': 'Lion', 'size': 'large'},
    45: {'name': 'Lizard', 'size': 'small'},
    46: {'name': 'Lobster', 'size': 'small'},
    47: {'name': 'Mosquito', 'size': 'small'},
    48: {'name': 'Moth', 'size': 'small'},
    49: {'name': 'Mouse', 'size': 'small'},
    50: {'name': 'Octopus', 'size': 'medium'},
    51: {'name': 'Okapi', 'size': 'large'},
    52: {'name': 'Orangutan', 'size': 'large'},
    53: {'name': 'Otter', 'size': 'small'},
    54: {'name': 'Owl', 'size': 'small'},
    55: {'name': 'Ox', 'size': 'large'},
    56: {'name': 'Oyster', 'size': 'small'},
    57: {'name': 'Panda', 'size': 'large'},
    58: {'name': 'Parrot', 'size': 'small'},
    59: {'name': 'Pelecaniformes', 'size': 'medium'},
    60: {'name': 'Penguin', 'size': 'small'},
    61: {'name': 'Pig', 'size': 'medium'},
    62: {'name': 'Pigeon', 'size': 'small'},
    63: {'name': 'Porcupine', 'size': 'small'},
    64: {'name': 'Possum', 'size': 'small'},
    65: {'name': 'Raccoon', 'size': 'small'},
    66: {'name': 'Rat', 'size': 'small'},
    67: {'name': 'Reindeer', 'size': 'large'},
    68: {'name': 'Rhinoceros', 'size': 'large'},
    69: {'name': 'Sandpiper', 'size': 'small'},
    70: {'name': 'Seahorse', 'size': 'small'},
    71: {'name': 'Seal', 'size': 'large'},
    72: {'name': 'Shark', 'size': 'large'},
    73: {'name': 'Sheep', 'size': 'medium'},
    74: {'name': 'Snake', 'size': 'small'},
    75: {'name': 'Sparrow', 'size': 'small'},
    76: {'name': 'Squid', 'size': 'medium'},
    77: {'name': 'Squirrel', 'size': 'small'},
    78: {'name': 'Starfish', 'size': 'small'},
    79: {'name': 'Swan', 'size': 'medium'},
    80: {'name': 'Tiger', 'size': 'large'},
    81: {'name': 'Turkey', 'size': 'medium'},
    82: {'name': 'Turtle', 'size': 'small'},
    83: {'name': 'Whale', 'size': 'large'},
    84: {'name': 'Wolf', 'size': 'large'},
    85: {'name': 'Wombat', 'size': 'small'},
    86: {'name': 'Woodpecker', 'size': 'small'},
    87: {'name': 'Zebra', 'size': 'large'}
}

# Initialize GUI
root = Tk()
root.geometry('800x600')
root.title('Object Identifier')
root.configure(background='#CDCDCD')
label = Label(root, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(root)

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        frame = cv2.imread(file_path)
        classify(frame)

upload_button = Button(root, text="Upload Image", command=upload_image, padx=10, pady=5)
upload_button.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
upload_button.pack(side=BOTTOM, pady=20)

def send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password):
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Log in to the SMTP server
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())

# Replace 'COM6' with the serial port connected to your Arduino
ser = serial.Serial('COM6', 9600, timeout=1)

def turn_relay_on():
    ser.write(b'1')  # Send '1' to turn on the relay
    print("Relay turned ON")


def turn_relay_off():
    ser.write(b'0')  # Send '0' to turn off the relay
    print("Relay turned OFF")

def classify(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = image.resize((128, 128))
    image_tk = ImageTk.PhotoImage(image)

    # Display the image in the GUI
    sign_image.configure(image=image_tk)
    sign_image.image = image_tk

    # Preprocess and classify the image
    image_array = preprocess_image(frame)
    pred = detect_objects(image_array)
    print('pred', pred)
    label.configure(foreground='#FF0000', text=pred)

    detected_object=pred
    # Send the name of the detected object to Arduino
    # Convert the dictionary to the format "name:size"
    object_str = f"{detected_object['name']}:{detected_object['size']}"
    ser.write(object_str.encode())  # Encode the formatted string and send it over serial

    print("Sent detected object:", detected_object)

    # Control relay based on classification result
    if pred == 'Human':
        turn_relay_off()
    else:
        turn_relay_on()

    # Replace the following variables with your own values
    subject = str('Alert:')+str(pred)+str(' nearing your Farm')
    body = "Dear Owner,\n\n\t" + str(pred) + " captured near Zone 1.\n\tPlease take immediate action.\n\nRegards,\nAI Team"
    to_email = "wfranciska01@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "josevinoth83@gmail.com"
    sender_password = "gfrt qlnu rzgt ytba"

    # Call the function to send the email
    send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password)

    # if user_input.isdigit():  # Check if the input is a digit
    #     value = int(user_input)
    #     nodeMCU_ip = "192.168.1.100"
    #     if value == 0:
    #         try:
    #             relay_endpoint = "/deactivate_relay"  # Change this endpoint based on your NodeMCU code
    #             # Send an HTTP GET request to control the relay
    #             requests.get(f"http://{nodeMCU_ip}{relay_endpoint}")
    #         except Exception as e:
    #             print(f"Error: {e}")
    #     elif value == 1:
    #         try:
    #             relay_endpoint = "/activate_relay"  # Change this endpoint based on your NodeMCU code
    #             # Send an HTTP GET request to control the relay
    #             requests.get(f"http://{nodeMCU_ip}{relay_endpoint}")
    #
    #         except Exception as e:
    #             print(f"Error: {e}")
    #     else:
    #         print("Invalid input. Please enter 1 to activate or 0 to deactivate.")
    # else:
    #     print("Exiting the script.")

    # Clear the image after 5 seconds
    root.after(5000, clear_image)


def clear_image():
    sign_image.configure(image=None)
    # label.configure(text='')


def detect_objects(frame):
    predictions = model.predict(frame)
    predicted_class_index = np.argmax(predictions)
    detected_object = classes[predicted_class_index]

    return detected_object


def preprocess_image(frame):
    image_array = cv2.resize(frame, (128, 128))
    image_array = np.expand_dims(image_array, axis=0)
    image_array = image_array.astype('float32') / 255.0

    return image_array


def capture_and_process():
    cap = cv2.VideoCapture(0)  # Use the default camera (you may need to adjust the camera index)
    ret, frame = cap.read()

    classify(frame)

    cap.release()


capture_button = Button(root, text="Capture Image from Camera", command=capture_and_process, padx=10, pady=5)
capture_button.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
capture_button.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)
heading = Label(root, text="Identify the Creature", pady=20, font=('arial', 20, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()

root.mainloop()


