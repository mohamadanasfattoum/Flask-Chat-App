"""
This module implements a Flask-based chat application with real-time communication
using Flask-SocketIO. It provides the following functionality:
Routes:
    - `/`: Renders the chat interface (chat.html).
    - `/register`: Renders the registration interface (register.html).
    - `/login`: Renders the login interface (login.html).
    - `/logout`: Logs out the user and redirects to the login interface.
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
    - `SQLALCHEMY_DATABASE_URI`: Used to configure the database URI for SQLAlchemy.
Execution:
    - The application runs with Flask-SocketIO in debug mode when executed directly.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO , emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registrierung erfolgreich! Bitte logge dich ein.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Benutzername existiert bereits.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ungültige Anmeldedaten.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Erfolgreich ausgeloggt.', 'success')
    return redirect(url_for('login'))

@app.route('/chat')
def index():
    """
    Renders the chat interface.
    Returns:
        Rendered HTML template for the chat interface.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('Bitte logge dich ein, um den Chat zu betreten.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    return render_template('chat.html', user=user)

@socketio.on('join')
def join(data):
    """
    Event handler for joining a chat room.
    Args:
        data (dict): Contains the room name under the key 'room'.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'User {user.username} has joined the room: {room}'}, room=room)

@socketio.on('leave')
def leave(data):
    """
    Event handler for leaving a chat room.
    Args:
        data (dict): Contains the room name under the key 'room'.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'User {user.username} has left the room: {room}'}, room=room)

@socketio.on('message')
def message(data):
    """
    Event handler for sending a message to a chat room.
    Args:
        data (dict): Contains the room name under the key 'room' and the message under the key 'msg'.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    room = data['room']
    message = data['msg']
    emit('message', {'msg': message, 'user': user.username}, room=room)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
