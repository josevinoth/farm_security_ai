import os
import warnings

from keras.preprocessing import image
from keras.src.utils import np_utils
warnings.filterwarnings('ignore')
import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from keras import models
from keras.optimizers import Adam
from keras import losses
from keras import metrics
from keras.models import Sequential
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from PIL import Image
import tensorflow as tf
from keras.utils import to_categorical
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D, Dropout

########################## Step-1) Explore the Dataset#########################
test_dir='images/val_dir'
train_dir = "images/animals"

train_class_labels=os.listdir(train_dir)
# print(train_class_labels)
train_total=0
for label in train_class_labels:
    total=len(os.listdir(os.path.join(train_dir,label)))
    # print(label,total)
    train_total+=total
# print('Train Total',train_total)

nb_train_samples=train_total
num_classes=87
img_rows=128
img_cols=128
channel=3

# Preprocess the train data
data=[]
labels=[]
i=0
j=0
for label in train_class_labels:
    image_names_train=os.listdir(os.path.join(train_dir,label))
    total=len(image_names_train)
    # print("Train_Label", label)
    # print("Train_Total", total)
    for image_name in image_names_train:
        try:
            img=image.load_img(os.path.join(train_dir,label,image_name),target_size=(img_rows,img_rows,channel))
            img=image.img_to_array(img)
            img=img/255
            data.append(img)
            labels.append(j)
        except:
            pass
        i+=1
    j+=1
print("success")

########################## Explore sample Image#########################
# path = "images/animals/bee/3d28692ff1.jpg"
# img = Image.open(path)
# img = img.resize((30, 30))
# sr = np.array(img)
# plt.imshow(img)
# plt.show()

########################## Step-2 Split Dataset into train and test#########################
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
print("training shape: ",x_train.shape, y_train.shape)
print("testing shape: ",x_test.shape, y_test.shape)
y_train = to_categorical(y_train, 87)
y_test = to_categorical(y_test, 87)

########################## Step-3) Build a CNN model#########################
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5,5), activation="relu", input_shape=x_train.shape[1:]))
model.add(Conv2D(filters=32, kernel_size=(5,5), activation="relu"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(rate=0.25))
model.add(Conv2D(filters=64, kernel_size=(3,3), activation="relu"))
model.add(Conv2D(filters=64, kernel_size=(3,3), activation="relu"))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dropout(rate=0.5))
model.add(Dense(43, activation="softmax"))

########################## Step-4) Train and Validate the Model#########################
epochs = 15
history = model.fit(x_train, y_train, epochs=epochs, batch_size=64, validation_data=(x_test, y_test))
plt.figure(0)
plt.plot(history.history['accuracy'], label="Training accuracy")
plt.plot(history.history['val_accuracy'], label="val accuracy")
plt.title("Accuracy")
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.legend()
plt.figure(1)
plt.plot(history.history['loss'], label="training loss")
plt.plot(history.history['val_loss'], label="val loss")
plt.title("Loss")
plt.xlabel("epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()