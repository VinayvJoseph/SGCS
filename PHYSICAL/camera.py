# This script captures images using the RPi camera and displays predictions by collaborating with a ML model in google colab.

from picamera import PiCamera
from time import sleep
import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import storage
import RPi.GPIO as GPIO
import time

#Pin Assingment
GPIO.setmode(GPIO.BCM)
SWITCH = 21
LED_PIN_Organic = 10
LED_PIN_PMD = 9
LED_PIN_Paper = 11

GPIO.setup(SWITCH, GPIO.IN)
GPIO.setup(LED_PIN_Organic, GPIO.OUT)
GPIO.setup(LED_PIN_PMD, GPIO.OUT)
GPIO.setup(LED_PIN_Paper, GPIO.OUT)

LED_Organic = False; LED_PMD = False; LED_Paper = False

# Initialize Firebase with your service account credentials for both the Realtime Database and Storage
cred = credentials.Certificate("/home/digitaltwin/SGCS/storage_bucket.json")
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

# Initialise pi camera.
camera = PiCamera()

# Blink LED based on waste type.
def blinkLED(led_pin):
    for _ in range(10):
        # Turn the LED on
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.5)  # 0.5 seconds ON

        # Turn the LED off
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.5)  # 0.5 seconds OFF

while True:
        #if GPIO.input(SWITCH)==GPIO.HIGH:
            print("Capturing image in 3s...")
            sleep(3)
            start_time = time.time()

            camera.capture('/home/digitaltwin/SGCS/IMAGES/image.jpg')
            print("Image Captured")

            # Get a reference to the Firebase Storage bucket
            bucket = storage.bucket()

            # Path to the image you want to upload
            image_path = "/home/digitaltwin/SGCS/IMAGES/image.jpg"
            # Define the destination path in Firebase Storage
            destination_blob_name = "images/image.jpg"

            # Upload the image
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(image_path)
            print("Image uploaded to firebase")

            # Update STATUS node in real-time database to begin ML inference.
            ref = db.reference('/STATUS')
            data = "NEW"
            ref.set(data)
            print("Status updated to NEW")

            # Wait for Machine Learning Processing
            sleep(3)

            # Spin Lock
            while ref.get() != "PROCESSED":
                 pass

            print("Processing complete")

            # Obtain prediction output from real-time database
            out = db.reference('/OUTPUT')
            prediction = out.get()
            print("PREDICTION : ",prediction)

            # Calculate response time.
            end_time = time.time()
            response_time = end_time - start_time

            # Update STATUS node in Real-time Database.
            ref.set("OLD")
            print("Status updated to OLD")
            print(f"Response time: {response_time:.4f} seconds\n")

            # Logic to blink LED's based on prediction
            if prediction == 'Paper and Cardboard':
                blinkLED(LED_PIN_Paper)
            elif prediction == 'Plastic' or prediction == 'Aluminium' or prediction == 'Carton' or prediction == 'Other Plastics':
                blinkLED(LED_PIN_PMD)
            elif prediction == 'Organic Waste' or prediction == 'Textiles':
                blinkLED(LED_PIN_Organic)
            else:
                GPIO.output(LED_PIN_Organic, GPIO.HIGH)
                GPIO.output(LED_PIN_PMD, GPIO.HIGH)
                GPIO.output(LED_PIN_Paper, GPIO.HIGH)
                sleep(10)
                GPIO.output(LED_PIN_Organic, GPIO.LOW)
                GPIO.output(LED_PIN_PMD, GPIO.LOW)
                GPIO.output(LED_PIN_Paper, GPIO.LOW)

            # Captures images every 20 seconds due to the absence of a switch.
            sleep(20)

        # Else for when a switch is included.
        #else:
             #sleep(1)
