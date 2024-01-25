# Import necessary libraries
import tensorflow as tf
from keras import layers, models
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array, load_img
import numpy as np

# Define the CNN model
model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Print a summary of the model architecture
model.summary()

# Load and preprocess the image for testing
img_path = 'images/football.jpg'  # Replace with the path to your image
img = image.load_img(img_path, target_size=(150, 150))
img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0  # Normalize pixel values to be between 0 and 1

# Make predictions with the model
prediction = model.predict(img_array)

# Print the prediction result
if prediction[0, 0] > 0.5:
    print("The image is in class 1 (e.g., positive class).")
else:
    print("The image is in class 0 (e.g., negative class).")