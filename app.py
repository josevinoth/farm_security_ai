# app.py continued
import os

import h5py
from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import io
from PIL import Image

app = Flask(__name__)
model = load_model('Animal_Detection/model/full_model.h5')
model_path = 'Animal_Detection/model/full_model.h5'

def preprocess_image(file):
    img = Image.open(file.stream).convert("RGB")
    img = img.resize((128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Convert the NumPy array to a Python list
    img_list = img_array.tolist()

    return img_array

@app.route('/')
def index():
    return render_template('index_1.html')

@app.route('/detect', methods=['POST'])
def detect():
    # dictionary to label all traffic signs class.
    classes = { 0:'bee',
                1: 'beetle',
                2: 'bison',
                3: 'boar',
                4: 'butterfly',
                5: 'cat',
                6: 'caterpillar',
                7: 'chimpanzee',
                8: 'cockroach',
                9: 'cow',
                10: 'coyote',
                11: 'crab',
                12: 'crow',
                13: 'deer',
                14: 'dog',
                15: 'dolphin',
                16: 'donkey',
                17: 'dragonfly',
                18: 'duck',
                19: 'eagle',
                20: 'elephant',
                21: 'fire',
                22: 'flamingo',
                23: 'fly',
                24: 'fox',
                25: 'goat',
                26: 'goldfish',
                27: 'goose',
                28: 'gorilla',
                29: 'grasshopper',
                30: 'hamster',
                31: 'hare',
                32: 'hedgehog',
                33: 'hippopotamus',
                34: 'hornbill',
                35: 'horse',
                36: 'hummingbird',
                37: 'hyena',
                38: 'jellyfish',
                39: 'kangaroo',
                40: 'koala',
                41: 'ladybugs',
                42: 'leopard',
                43: 'lion',
                44: 'lizard',
                45: 'lobster',
                46: 'mosquito',
                47: 'moth',
                48: 'mouse',
                49: 'octopus',
                50: 'okapi',
                51: 'orangutan',
                52: 'otter',
                53: 'owl',
                54: 'ox',
                55: 'oyster',
                56: 'panda',
                57: 'parrot',
                58: 'pelecaniformes',
                59: 'penguin',
                60: 'pig',
                61: 'pigeon',
                62: 'porcupine',
                63: 'possum',
                64: 'raccoon',
                65: 'rat',
                66: 'reindeer',
                67: 'rhinoceros',
                68: 'sandpiper',
                69: 'seahorse',
                70: 'seal',
                71: 'shark',
                72: 'sheep',
                73: 'snake',
                74: 'sparrow',
                75: 'squid',
                76: 'squirrel',
                77: 'starfish',
                78: 'swan',
                79: 'tiger',
                80: 'turkey',
                81: 'turtle',
                82: 'whale',
                83: 'wolf',
                84: 'wombat',
                85: 'woodpecker',
                86: 'zebra',
    }

    if 'image' not in request.files:
        return render_template('index_1.html', error='No file provided')

    file = request.files['image']

    if file.filename == '':
        return render_template('index_1.html', error='No file selected')

    img_array = preprocess_image(file)
    prediction = model.predict(img_array)

    # Get the index of the highest probability
    predicted_class_index = np.argmax(prediction)
    detected_object=classes[predicted_class_index]
    return render_template('result.html', prediction=detected_object)

if __name__ == '__main__':
    app.run(debug=True)
