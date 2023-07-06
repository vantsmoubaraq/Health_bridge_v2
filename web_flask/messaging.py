from flask import Flask, render_template
from flask_socketio import SocketIO, send
import secrets
from models import storage
from models.users import User 

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(32)
socketio = SocketIO(app, cors_allowed_origins="*")
app.debug = True

@app.route('/chat')
def index():
    return render_template('messaging.html')

@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data)
    if data != "I\'m connected!":
        send(data, broadcast=True)
    #socketio.emit('message', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)