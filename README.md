# Flask Chat App

This is a simple Flask-based chat application that enables real-time communication using Flask-SocketIO. Users can join chat rooms, send messages, and leave rooms seamlessly.

## Features

- Real-time communication using WebSockets.
- Join and leave chat rooms dynamically.
- Broadcast messages to all users in a room.
- Simple and intuitive user interface.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd flask-chat-app/src
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirement.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Use the interface to join a chat room, send messages, and leave the room.

## Project Structure

```
flask-chat-app/src
├── app.py               # Main application file
├── befehle.md           # Command reference for setup
├── requirement.txt      # Python dependencies
├── templates/
│   └── chat.html        # HTML template for the chat interface
└── __pycache__/         # Compiled Python files (ignored in version control)
```

## Technologies Used

- Flask
- Flask-SocketIO
- HTML/CSS (Bootstrap)
- JavaScript


## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)