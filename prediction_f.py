# app.py continued
from flask import request, render_template, app
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

model = load_model('C:\Users\BVM\PycharmProjects\farm_security_ai\model\full_model.h5')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return render_template('index_1.html', error='No file provided')

    file = request.files['image']

    if file.filename == '':
        return render_template('index_1.html', error='No file selected')

    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)
    # Process the prediction result as needed

    return render_template('result.html', prediction=prediction)
