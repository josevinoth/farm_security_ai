import cv2
import numpy as np
from keras.applications import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from keras.preprocessing import image

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

# Load an image
image_path = '../images/animals/bison/1e92525212.jpg'
img = image.load_img(image_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Predict
predictions = model.predict(x)
predicted_labels = decode_predictions(predictions)

# Display the top 5 predictions
for i, (imagenet_id, label, score) in enumerate(predicted_labels[0]):
    print(f"{i + 1}: {label} ({score:.2f})")

# Draw the prediction on the image
img = cv2.imread(image_path)
img = cv2.resize(img, (224, 224))
cv2.putText(img, f"Prediction: {predicted_labels[0][0][1]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
