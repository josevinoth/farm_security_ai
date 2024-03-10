from tkinter import *

import requests
from PIL import ImageTk, Image
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
import cv2
import serial
import time

# Load the trained model to classify Animals
model = load_model('../model/full_model.h5')

# Dictionary to label all traffic signs class.
classes = {0:'Bee',
1: 'Beetle',
2: 'Bison',
3: 'Boar',
4: 'Butterfly',
5: 'Cat',
6: 'Caterpillar',
7: 'Chimpanzee',
8: 'Cockroach',
9: 'Cow',
10: 'Coyote',
11: 'Crab',
12: 'Crow',
13: 'Deer',
14: 'Dog',
15: 'Dolphin',
16: 'Donkey',
17: 'Dragonfly',
18: 'Duck',
19: 'Eagle',
20: 'Elephant',
21: 'Fire',
22: 'Flamingo',
23: 'Fly',
24: 'Fox',
25: 'Goat',
26: 'Goldfish',
27: 'Goose',
28: 'Gorilla',
29: 'Grasshopper',
30: 'Hamster',
31: 'Hare',
32: 'Hedgehog',
33: 'Hippopotamus',
34: 'Hornbill',
35: 'Horse',
36: 'Human',
37: 'Hummingbird',
38: 'Hyena',
39: 'Jellyfish',
40: 'Kangaroo',
41: 'Koala',
42: 'Ladybugs',
43: 'Leopard',
44: 'Lion',
45: 'Lizard',
46: 'Lobster',
47: 'Mosquito',
48: 'Moth',
49: 'Mouse',
50: 'Octopus',
51: 'Okapi',
52: 'Orangutan',
53: 'Otter',
54: 'Owl',
55: 'Ox',
56: 'Oyster',
57: 'Panda',
58: 'Parrot',
59: 'Pelecaniformes',
60: 'Penguin',
61: 'Pig',
62: 'Pigeon',
63: 'Porcupine',
64: 'Possum',
65: 'Raccoon',
66: 'Rat',
67: 'Reindeer',
68: 'Rhinoceros',
69: 'Sandpiper',
70: 'Seahorse',
71: 'Seal',
72: 'Shark',
73: 'Sheep',
74: 'Snake',
75: 'Sparrow',
76: 'Squid',
77: 'Squirrel',
78: 'Starfish',
79: 'Swan',
80: 'Tiger',
81: 'Turkey',
82: 'Turtle',
83: 'Whale',
84: 'Wolf',
85: 'Wombat',
86: 'Woodpecker',
87: 'Zebra',}

# Initialize GUI
root = Tk()
root.geometry('800x600')
root.title('Object Identifier')
root.configure(background='#CDCDCD')
label = Label(root, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(root)

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

    if pred == 'Human':
        user_input = '0'
    else:
        user_input = '1'

    if user_input.isdigit():  # Check if the input is a digit
        value = int(user_input)
        if value == 0:
            try:
                nodeMCU_ip = "192.168.1.23"
                relay_endpoint = "/deactivate_relay"  # Change this endpoint based on your NodeMCU code
                # Send an HTTP GET request to control the relay
                requests.get(f"http://{nodeMCU_ip}{relay_endpoint}")
            except Exception as e:
                print(f"Error: {e}")
        elif value == 1:
            try:
                nodeMCU_ip = "192.168.1.23"
                relay_endpoint = "/activate_relay"  # Change this endpoint based on your NodeMCU code
                # Send an HTTP GET request to control the relay
                requests.get(f"http://{nodeMCU_ip}{relay_endpoint}")

            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid input. Please enter 1 to activate or 0 to deactivate.")
    else:
        print("Exiting the script.")

    # # Arduino communication (replace with your logic)
    # arduino_port = "COM3"
    # baud_rate = 9600
    # ser = serial.Serial(arduino_port, baud_rate)
    # time.sleep(2)
    # if pred == 'Human':
    #     object_id = '0'
    # else:
    #     object_id = '1'
    # user_input = object_id
    # if user_input == '1' or user_input == '0':
    #     ser.write(user_input.encode())
    #     print("Exiting the script")
    #     ser.close()
    # else:
    #     print("Invalid input. Enter '1' or '0'.")
    #     ser.close()

    # Clear the image after 5 seconds
    # root.after(5000, clear_image)


# def clear_image():
#     sign_image.configure(image=None)
#     # label.configure(text='')


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