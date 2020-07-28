from flask import Flask, render_template        #install flask + flask-socketio
from flask_socketio import SocketIO
import time
import RPi.GPIO as GPIO 
import os
import glob

# creates a Flask application, named app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# create a SocketIO(app)
socketio = SocketIO(app)

# create port (?)
PORT = 5000
print("Server is starting at port 5000...")

# a route where we will display a welcome message via an HTML template
@app.route("/", methods = ['GET', 'POST'])
def hello():
    return render_template('index.html')

# functions to control the lights
GPIO.setwarnings(False) 
LED_PIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
status = 0
def onLight():
    global status
    GPIO.output(LED_PIN, GPIO.HIGH)
    status = "On"
    socketio.emit("lightOn", {'data': 'From server: The light: On'})

def offLight():
    global status
    GPIO.output(LED_PIN, GPIO.LOW)
    status = "Off"
    socketio.emit("lightOff", {'data': 'From server: The light: Off'})

# socket on connection
@socketio.on('connection')
def connection(data):
    if (status != 0):
        socketio.emit(f"light{status}", {'data': f'From server: The light: {status}'})
    print(data)

# socketio - functions to control light
@socketio.on('turn-on')
def turnOn(data):
    print(data)
    onLight()             #put the def to control the light here!

@socketio.on('turn-off')
def turnOn(data):
    print(data)
    offLight()            #put the def to control the light here!

# Function for temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

@socketio.on('temp')
def temp(data):
    while True:
        tempC, tempF = read_temp()
        socketio.emit("temp", {"tempC": "{:.2f}".format(tempC)}, {"tempF": "{:.2f}".format(tempF)})
        
# run the application ** socketio.run(app)
if __name__ == "__main__":
    socketio.run(app)