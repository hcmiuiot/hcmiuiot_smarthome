from flask import Flask, render_template        #install flask + flask-socketio
from flask_socketio import SocketIO

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
    return render_template('LED.html')

# socket on connection
@socketio.on('connection')
def connection(data):
    print(data)

# functions to control the lights
    def onLight():
        print("Code turn on here!")
        socketio.emit("lightOn", {'data': 'On'})

    def offLight():
        print("Code turn off here!")
        socketio.emit("lightOff", {'data': 'Off'})

    # socketio - functions to control light
    @socketio.on('turn-on')
    def turnOn(data):
        print(data)
        onLight()             #put the def to control the light here!

    @socketio.on('turn-off')
    def turnOff(data):
        print(data)
        offLight()            #put the def to control the light here!

# function to send the temperature information
@socketio.on('temp-inf')
    def sendTempInf('data'):
        print(data)
        temp = getTempInf()
        socketio.emit('temp-inf', {'data': temp})

# ras func
    def getTempInf():
        print('Get temp inf here')

# run the application ** socketio.run(app)
if __name__ == "__main__":
    socketio.run(app)