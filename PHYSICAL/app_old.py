# SGCS application code.

import asyncio
import websockets
import json
import tkinter as tk
from threading import Thread
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, db
import datetime
import random

# Configurable parameters
server_ip = "131.155.221.7" # Server IP address
port = 8080 # Websocket port
database_upload_interval = 300 # Uploads every 5 minutes
bin_height = 42.0 #cm

# Global variables to store sensor data
t1=0.0; h1=0.0; d1=0.0; t2=0.0; h2=0.0; d2=0.0; t3=0.0; h3=0.0; d3=0.0;
DB=[1,1,1,1,1,1,1,1,1] # variable to decide which sensor data is uploaded to the cloud
simulation_flag = 0 # Simulation/Physical mode flag
LED_Organic = False; LED_PMD = False; LED_Paper = False ;

# JSON message key/value pair initialisation.
sensor_reading = {
    'Timestamp': '',
    'Temperature_Organic': t1,
    'Humidity_Organic': h1,
    'Distance_Organic': d1,
    'Temperature_PMD': t2,
    'Humidity_PMD': h2,
    'Distance_PMD': d2,
    'Temperature_Paper': t3,
    'Humidity_Paper': h3,
    'Distance_Paper': d3,
    'Organic_isFull': LED_Organic,
    'PMD_isFull' : LED_PMD,
    'Paper_isFull': LED_Paper
}

# Pin Assingment
GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_Organic = 2
DHT_PIN_PMD = 3
DHT_PIN_Paper = 4

GPIO_TRIGGER_Organic = 17
GPIO_ECHO_Organic = 18
GPIO_TRIGGER_PMD = 27
GPIO_ECHO_PMD = 23
GPIO_TRIGGER_Paper = 22
GPIO_ECHO_Paper = 24

LED_PIN_Organic = 10
LED_PIN_PMD = 9
LED_PIN_Paper = 11

#Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_Organic, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Organic, GPIO.IN)
GPIO.setup(DHT_PIN_Organic, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_PMD, GPIO.OUT)
GPIO.setup(GPIO_ECHO_PMD, GPIO.IN)
GPIO.setup(DHT_PIN_PMD, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_Paper, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Paper, GPIO.IN)
GPIO.setup(DHT_PIN_Paper, GPIO.IN)
GPIO.setup(LED_PIN_Organic, GPIO.OUT)
GPIO.setup(LED_PIN_PMD, GPIO.OUT)
GPIO.setup(LED_PIN_Paper, GPIO.OUT)

# Websocket Communication with Unity(websocket client)
async def server(websocket, path):
    print("Server Running on port : ", port)
    global sensor_reading, t1, h1, d1, t2, h2, d2, t3, h3, d3, simulation_flag, LED_Organic, LED_PMD, LED_Paper;

    try:
        while True:
            if simulation_flag==0:
                current_time = datetime.datetime.now()
                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

                '''
                try:
                    h1r, t1r = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_Organic, retries=2)
                    if h1r is not None and t1r is not None:
                        # Data reading was successful, round the values
                        h1 = round(h1r, 3)
                        t1 = round(t1r, 3)
                    else:
                        # Data reading failed, handle the error
                        t1=999; h1=999;
                        print("Failed to read Organic DHT sensor.")
                except Exception as e:
                    # Handle exceptions (e.g., timeout or other errors)
                    print(f"Error reading Organic sensor data: {str(e)}")
                '''

                try:
                    h2r, t2r = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_PMD, retries=3)
                    if h2r is not None and t2r is not None:
                        h2 = round(h2r, 3)
                        t2 = round(t2r, 3)
                    else:
                        t2=999; h2=999;
                        print("Failed to read PMD DHT sensor.")
                except Exception as e:
                    print(f"Error reading PMD sensor data: {str(e)}")

                try:
                    h3r, t3r = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN_Paper, retries=4)
                    if h3r is not None and t3r is not None:
                        h3 = round(h3r, 3)
                        t3 = round(t3r, 3)
                    else:
                        t3=999; h3=999;
                        print("Failed to read Paper DHT sensor.")
                except Exception as e:
                    print(f"Error reading Paper sensor data: {str(e)}")

                # Level Measurement with ultrasonic sensors
                d1r = distance(GPIO_TRIGGER_Organic, GPIO_ECHO_Organic)
                d1 = round(100-(d1r/bin_height*100),3);
                time.sleep(0.1)
                d2r = distance(GPIO_TRIGGER_PMD, GPIO_ECHO_PMD)
                d2 = round(100-(d2r/bin_height*100),3);
                time.sleep(0.1)
                d3r = distance(GPIO_TRIGGER_Paper, GPIO_ECHO_Paper)
                d3 = round(100-(d3r/bin_height*100),3);
                time.sleep(0.1)

                # Send continuous data to the client
                sensor_reading = {
                'Timestamp' : current_time_str,
                'Temperature_Organic': t1,
                'Humidity_Organic': h1,
                'Distance_Organic': d1,
                'Temperature_PMD': t2,
                'Humidity_PMD': h2,
                'Distance_PMD': d2,
                'Temperature_Paper': t3,
                'Humidity_Paper': h3,
                'Distance_Paper': d3,
                'Organic_isFull': LED_Organic,
                'PMD_isFull' : LED_PMD,
                'Paper_isFull': LED_Paper
                }

                await websocket.send(json.dumps(sensor_reading))
                await asyncio.sleep(0.2)  # Adjust the interval as needed

            # Wait for data from the client (non-blocking)
            try:
                data_from_client = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                if data_from_client == "Simulation Mode" and simulation_flag==0:
                    simulation_flag = 1
                    print(f"Received from client: {data_from_client}")

                if simulation_flag == 1:
                    client_data = await websocket.recv()
                    if client_data == "Physical Mode":
                        simulation_flag = 0
                        print(f"Received from client: {client_data}")
                        continue

                    # Receiving json data from Unity.
                    data = json.loads(client_data)
                    print("Receiving Data from Unity")

                    # Storing Unity data into global varibales.
                    t1 = data['Temperature_Organic'];h1 = data['Humidity_Organic'];d1 = data['Distance_Organic']; LED_Organic = data['Organic_isFull'];
                    t2 = data['Temperature_PMD']; h2 = data['Humidity_PMD']; d2 = data['Distance_PMD']; LED_PMD = data['PMD_isFull'];
                    t3 = data['Temperature_Paper']; h3 = data['Humidity_Paper']; d3 = data['Distance_Paper']; LED_Paper = data['Paper_isFull'];

            except asyncio.TimeoutError:
                pass

            # Updating LEDs
            if d1>75:
                LED_Organic = True
            else:
                LED_Organic = False
            if d2>75:
                LED_PMD = True
            else:
                LED_PMD = False
            if d3>75:
                LED_Paper = True
            else:
                LED_Paper = False

            GPIO.output(LED_PIN_Organic, LED_Organic)
            GPIO.output(LED_PIN_PMD, LED_PMD)
            GPIO.output(LED_PIN_Paper, LED_Paper)


    except websockets.ConnectionClosed:
        print("Client disconnected")

# Function to update the AMOLED Waveshare display.
def update_label_data():
    global t1, h1, d1, t2, h2, d2, t3, h3, d3, simulation_flag;
    while True:
        t1_label.config(text=f"Temperature Organic: {t1:.2f}°C")
        h1_label.config(text=f"Humidity Organic: {h1:.2f}%")
        d1_label.config(text=f"Level Organic {d1:.2f}%")
        t2_label.config(text=f"Temperature PMD: {t2:.2f}°C")
        h2_label.config(text=f"Humidity PMD: {h2:.2f}%")
        d2_label.config(text=f"Level PMD {d2:.2f}%")
        t3_label.config(text=f"Temperature Paper: {t3:.2f}°C")
        h3_label.config(text=f"Humidity Paper: {h3:.2f}%")
        d3_label.config(text=f"Level Paper {d3:.2f}%")

        if simulation_flag == 0:
            mode_label.config(text="PHYSICAL MODE")
            root.configure(background="lightblue")
        else:
            mode_label.config(text="SIMULATION MODE")
            root.configure(background="yellow")

        time.sleep(3)

# Function to upload sensor data to the real-time database in firebase.
def upload_database():
    global sensor_reading, database_upload_interval, DB;
    Key = ['Temperature_Organic', 'Humidity_Organic', 'Distance_Organic','Temperature_PMD', 'Humidity_PMD', 'Distance_PMD','Temperature_Paper', 'Humidity_Paper', 'Distance_Paper']
    while True:
        time.sleep(database_upload_interval)
        database_reading ={'Timestamp':sensor_reading['Timestamp']}
        Value = [sensor_reading[Key[0]], sensor_reading[Key[1]], sensor_reading[Key[2]],sensor_reading[Key[3]], sensor_reading[Key[4]], sensor_reading[Key[5]],
                 sensor_reading[Key[6]], sensor_reading[Key[7]], sensor_reading[Key[8]]]
        
        # Data selection based on input from display
        for i in range(9):
            if DB[i]!=0:
                database_reading[Key[i]] = Value[i]

        # Send data to the database
        if database_reading["Timestamp"] == '' :
            continue;
        ref.child(database_reading['Timestamp']).set(database_reading)
        print("Data sent to firebase")
        database_reading = {}

# Function to measure distance using ultraosnic sensors
def distance(trigger, echo):
    
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(echo) == 0:
        StartTime = time.time()
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

# Function to flip background colour of ON/OFF buttons on the display.
def toggle_led_color(button, label, index):
    global tdb, hdb, ddb;
    current_color = button.cget("bg")
    new_color = "red" if current_color == "green" else "green"
    button.config(bg=new_color)

    if new_color == "red":
        button.config(text="OFF")
        DB[index-1] = 0

    else:
        button.config(text="ON")
        DB[index-1] = 1

# Initialize Firebase Admin SDK with your downloaded credentials
cred = credentials.Certificate('/home/digitaltwin/SGCS/firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgcs-1f60d-default-rtdb.firebaseio.com/'
})

ref = db.reference('Sensor_Data')

# Start server
start_server = websockets.serve(server, server_ip, port)

# Create event loop
loop = asyncio.get_event_loop()

# Create Tkinter GUI
root = tk.Tk()
root.title("SGCS Data")

# Display labels and buttons
t1_label = tk.Label(root, text="Temperature Organic: N/A", font=("Helvetica", 50))
t1_label.grid(row=0, column=1, padx=0, pady=0, sticky="w")
t1_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(t1_led_button, t1_label, 1), font=("Helvetica", 60))
t1_led_button.grid(row=0, column=0, padx=0, pady=0)
#
h1_label = tk.Label(root, text="Humidity Organic: N/A", font=("Helvetica", 50))
h1_label.grid(row=1, column=1, padx=0, pady=0, sticky="w")
h1_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(h1_led_button, h1_label, 2), font=("Helvetica", 60))
h1_led_button.grid(row=1, column=0, padx=0, pady=0)
#
d1_label = tk.Label(root, text="Level Organic: N/A", font=("Helvetica", 50))
d1_label.grid(row=2, column=1, padx=0, pady=0, sticky="w")
d1_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(d1_led_button, d1_label, 3), font=("Helvetica", 60))
d1_led_button.grid(row=2, column=0, padx=0, pady=0)

t2_label = tk.Label(root, text="Temperature PMD: N/A", font=("Helvetica", 50))
t2_label.grid(row=3, column=1, padx=0, pady=0, sticky="w")
t2_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(t2_led_button, t2_label, 4), font=("Helvetica", 60))
t2_led_button.grid(row=3, column=0, padx=0, pady=0)
#
h2_label = tk.Label(root, text="Humidity PMD: N/A", font=("Helvetica", 50))
h2_label.grid(row=4, column=1, padx=0, pady=0, sticky="w")
h2_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(h2_led_button, h2_label, 5), font=("Helvetica", 60))
h2_led_button.grid(row=4, column=0, padx=0, pady=0)
#
d2_label = tk.Label(root, text="Level PMD: N/A", font=("Helvetica", 50))
d2_label.grid(row=5, column=1, padx=0, pady=0, sticky="w")
d2_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(d2_led_button, d2_label, 6), font=("Helvetica", 60))
d2_led_button.grid(row=5, column=0, padx=0, pady=0)

t3_label = tk.Label(root, text="Temperature Paper: N/A", font=("Helvetica", 50))
t3_label.grid(row=6, column=1, padx=0, pady=0, sticky="w")
t3_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(t3_led_button, t3_label, 7), font=("Helvetica", 60))
t3_led_button.grid(row=6, column=0, padx=0, pady=0)
#
h3_label = tk.Label(root, text="Humidity Paper: N/A", font=("Helvetica", 50))
h3_label.grid(row=7, column=1, padx=0, pady=0, sticky="w")
h3_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(h3_led_button, h3_label, 8), font=("Helvetica", 60))
h3_led_button.grid(row=7, column=0, padx=0, pady=0)
#
d3_label = tk.Label(root, text="Level Paper: N/A", font=("Helvetica", 50))
d3_label.grid(row=8, column=1, padx=0, pady=0, sticky="w")
d3_led_button = tk.Button(root, text="ON", bg="green", command=lambda: toggle_led_color(d3_led_button, d3_label, 9), font=("Helvetica", 60))
d3_led_button.grid(row=8, column=0, padx=0, pady=0)

mode_label = tk.Label(root, text="", font=("Helvetica", 50))
mode_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Function to start websocket communication event loop in a separate thread
def start_event_loop():
    loop.run_until_complete(start_server)
    loop.run_forever()

# Start the event loop in a separate thread. Three different threads are created and initiated.
event_loop_thread = Thread(target=start_event_loop)
display_thread = Thread(target=update_label_data)
upload_thread = Thread(target=upload_database)
event_loop_thread.start() # Beginning execution of Websocket communication thread.
display_thread.start() # Beginning execution of displaying variables on Waveshare thread.
upload_thread.start() # Beginning execution of database upload to Firebase thread.

# Start Tkinter main loop
root.mainloop() # Blocking code which checks for updates on the tkinter display.
