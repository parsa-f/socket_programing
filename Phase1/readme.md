# Python Socket Chat

A minimal command-line chat application using Python sockets.

## How It Works

### Server (`server.py`)
```python
# Core functionality:
server_socket.bind((HOST, PORT))  # Binds to local IP
server_socket.listen()            # Waits for connection
client_socket.send()/recv()       # Handles message exchange

Client (client.py)
# Core functionality: 
client_socket.connect((HOST, PORT))  # Connects to server
client_socket.send()/recv()         # Sends/receives messages

Key Features
Single client-server connection

Basic message exchange

/exit command to quit

Localhost operation (127.0.0.1)

##Setup
Install requirements:

bash

pip install termcolor
Run in separate terminals:

bash

# Terminal 1:
python server.py

# Terminal 2: 
python client.py

Usage Notes
Type messages in either terminal

First run server, then client

Use /exit to close connection

Colored output works best in Linux/Mac terminals

Technical Specs
Protocol: TCP/IP

Port: 12345

Encoding: UTF-8

Buffer: 1024 bytes