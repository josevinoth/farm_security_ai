from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from keras.models import load_model
import numpy as np
from keras.preprocessing import image

#load the trained model to classify Animals
model = load_model('../model/full_model.h5')
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
                36: 'Hummingbird',
                37: 'Hyena',
                38: 'Jellyfish',
                39: 'Kangaroo',
                40: 'Koala',
                41: 'Ladybugs',
                42: 'Leopard',
                43: 'Lion',
                44: 'Lizard',
                45: 'Lobster',
                46: 'Mosquito',
                47: 'Moth',
                48: 'Mouse',
                49: 'Octopus',
                50: 'Okapi',
                51: 'Orangutan',
                52: 'Otter',
                53: 'Owl',
                54: 'Ox',
                55: 'Oyster',
                56: 'Panda',
                57: 'Parrot',
                58: 'Pelecaniformes',
                59: 'Penguin',
                60: 'Pig',
                61: 'Pigeon',
                62: 'Porcupine',
                63: 'Possum',
                64: 'Raccoon',
                65: 'Rat',
                66: 'Reindeer',
                67: 'Rhinoceros',
                68: 'Sandpiper',
                69: 'Seahorse',
                70: 'Seal',
                71: 'Shark',
                72: 'Sheep',
                73: 'Snake',
                74: 'Sparrow',
                75: 'Squid',
                76: 'Squirrel',
                77: 'Starfish',
                78: 'Swan',
                79: 'Tiger',
                80: 'Turkey',
                81: 'Turtle',
                82: 'Whale',
                83: 'Wolf',
                84: 'Wombat',
                85: 'Woodpecker',
                86: 'Zebra',}
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
    # pred = 'Fire'
    # sign = classes[pred]
    # print(sign)
    label.configure(foreground='#011638', text=pred)
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
    print('predictions',predictions)
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