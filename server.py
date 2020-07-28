from flask import Flask, render_template        #install flask + flask-socketio
from flask_socketio import SocketIO
import time
import RPi.GPIO as GPIO 

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
    GPIO.output(LED_PIN, GPIO.HIGH)
    status = "On"
    socketio.emit("lightOn", {'data': 'From server: The light: On'})

def offLight():
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

# run the application ** socketio.run(app)
if __name__ == "__main__":
    socketio.run(app)