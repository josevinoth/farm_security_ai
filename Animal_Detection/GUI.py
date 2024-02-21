from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
import serial
import time

#load the trained model to classify Animals
model = load_model('model/full_model_old.h5')
#dictionary to label all traffic signs class.
classes = { 0:'Bee',
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


#initialize GUI
top=tk.Tk()
top.geometry('800x600')
top.title('Object Identifier')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)
def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((248,248))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    # pred = model.predict([image])[0]
    pred = detect_objects(file_path)
    print('pred',pred)
    # pred = 'Fire'
    # sign = classes[pred]
    # print(sign)
    label.configure(foreground='#FF0000', text=pred)

    arduino_port = "COM3"  # Replace with your actual COM port (e.g., COM3)
    baud_rate = 9600
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Allow time for Arduino to reset
    if pred == 'Beetle':
        object_id = '1'
    else:
        object_id = '0'
    user_input = object_id
    if user_input == '1' or user_input == '0':
        # time.sleep(1)
        ser.write(user_input.encode())
        # time.sleep(1)
        print("Exiting the script")
        ser.close()
    else:
        print("Invalid input. Enter '1' or '0'.")
        ser.close()
def show_classify_button(file_path):
    classify_b=Button(top,text="Classify Image",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)

def preprocess_image(file):
    # img = Image.open(file.stream).convert("RGB")
    if isinstance(file, str):  # If the input is a file path
        img = Image.open(file).convert("RGB")
    else:  # If the input is a file object
        img = Image.open(file.stream).convert("RGB")
    img = img.resize((128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Convert the NumPy array to a Python list
    img_list = img_array.tolist()

    return img_array

def detect_objects(file_path):
    # Preprocess the image
    image_array = preprocess_image(file_path)

    # Perform object detection
    predictions = model.predict(image_array)
    # Get the index of the highest probability
    predicted_class_index = np.argmax(predictions)
    detected_object = classes[predicted_class_index]
    # Process the predictions as needed for your specific use case
    # (e.g., getting the class with the highest probability)
    print('predicted_class_index',predicted_class_index)
    print('detected_object',detected_object)
    return detected_object

# def classify(file_path):
#     global label_packed
#     predictions = detect_objects(file_path)
#     # Process predictions and update the GUI as needed
#     # (e.g., updating a label with the detected object class)
#     label.configure(foreground='#011638', text=predictions)
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass
upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Identify the Creature",pady=20, font=('arial',20,'bold'))
heading.configure(background='#CDCDCD',foreground='#364156')
heading.pack()
top.mainloop()