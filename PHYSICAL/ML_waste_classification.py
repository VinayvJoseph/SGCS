# Machine Learning model for Waste Classification
# Code to be run only in google colab environment.

# CELL 1
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import os
import cv2
from google.colab import files
import requests
from tensorflow.keras.models import load_model
from PIL import Image
from google.colab import files
import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import storage
from google.colab.patches import cv2_imshow
from time import sleep

# Use the files.upload() function to upload an image. Upload ServiceAccountKey.json
uploaded = files.upload()

# WasteClassification repository
!git clone https://github.com/cardstdani/WasteClassificationNeuralNetwork.git

#LOAD DATA
DIR = "/content/WasteClassificationNeuralNetwork/WasteImagesDataset"
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(DIR, validation_split=0.1, subset="training", seed=42, batch_size=128, smart_resize=True, image_size=(256, 256))
test_dataset = tf.keras.preprocessing.image_dataset_from_directory(DIR, validation_split=0.1, subset="validation", seed=42, batch_size=128, smart_resize=True, image_size=(256, 256))

classes = train_dataset.class_names
numClasses = len(train_dataset.class_names)
print(classes)

# Initialize Firebase with your service account credentials for both the Realtime Database and Storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgcs-1f60d-default-rtdb.firebaseio.com/',
    'storageBucket': 'sgcs-1f60d.appspot.com'
})

# Verify Realtime Database Access
try:
    ref = db.reference('/')
    data = ref.get()
    print("Realtime Database Access Verified.")
except Exception as e:
    print(f"Error accessing Realtime Database: {e}")

# Verify Cloud Storage (Storage Bucket) Access
try:
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    print("Cloud Storage Access Verified.")
except Exception as e:
    print(f"Error accessing Cloud Storage: {e}")

'''-----------------------------------------------------------------------------------------------------------'''

# CELL 2
# Begin inference based on images capture by raspberry pi.
while True:
    ref = db.reference('/STATUS')  # STATUS node is monitored for newer images.

    # Read data from the specified location
    data = ref.get()

    if(data == "NEW"):
        print("Processing new image")
        out = db.reference('OUTPUT')
        # Retrieve image from firebase
        bucket = storage.bucket('sgcs-1f60d.appspot.com')
        blob = bucket.get_blob("images/image.jpg")

        arr = np.frombuffer(blob.download_as_string(), np.uint8)
        input_img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

        # Load the pre-trained model
        model = load_model('/content/WasteClassificationNeuralNetwork/WasteClassificationModel.h5')

        # Resize the input image to match the model's input shape (256x256)
        img_array_resized = tf.image.resize(input_img, (256, 256))
        # Expand the dimensions to create a batch of one image
        img_array_resized = tf.expand_dims(img_array_resized, 0)

        # Prediction
        predictions = model.predict(img_array_resized)
        print("Prediction complete")

        # Write to database
        out.set(classes[np.argmax(predictions)])
        print("Uploaded prediction to database")
        ref.set("PROCESSED")
        print("Updated status to PROCESSED")

        # Output
        cv2_imshow(input_img)
        #plt.imshow(input_img)
        print(predictions[0]*100, "\n", classes)
        print("Prediction: ", classes[np.argmax(predictions)], f"{predictions[0][np.argmax(predictions)]*100}%")
        sleep(5)

    else:
        # Poll database for updates every three seconds.
        sleep(3)


