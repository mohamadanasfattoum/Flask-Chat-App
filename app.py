"""
This module implements a Flask-based chat application with real-time communication
using Flask-SocketIO. It provides the following functionality:
Routes:
    - `/`: Renders the chat interface (chat.html).
SocketIO Events:
    - `join`: Allows a user to join a specific chat room. Broadcasts a message to the room
      notifying that the user has joined.
        Args:
            data (dict): Contains the room name under the key 'room'.
    - `leave`: Allows a user to leave a specific chat room. Broadcasts a message to the room
      notifying that the user has left.
        Args:
            data (dict): Contains the room name under the key 'room'.
    - `message`: Handles sending messages to a specific chat room. Broadcasts the message
      to all users in the room.
        Args:
            data (dict): Contains the room name under the key 'room' and the message under
            the key 'msg'.
Configuration:
    - `SECRET_KEY`: Used to configure the Flask application for session management.
Execution:
    - The application runs with Flask-SocketIO in debug mode when executed directly.
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO , emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    """
    Renders the chat interface.
    Returns:
        Rendered HTML template for the chat interface.
    """
    return render_template('chat.html')

@socketio.on('join')
def handle_join(data):
    """
    Event handler for joining a chat room.
    Args:
        data (dict): Contains the room name under the key 'room'.
    """
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'User has joined the room: {room}'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    """
    Event handler for leaving a chat room.
    Args:
        data (dict): Contains the room name under the key 'room'.
    """
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'User has left the room: {room}'}, room=room)

@socketio.on('message')
def handle_message(data):
    """
    Event handler for sending a message to a chat room.
    Args:
        data (dict): Contains the room name under the key 'room' and the message under the key 'msg'.
    """
    room = data['room']
    message = data['msg']
    emit('message', {'msg': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
