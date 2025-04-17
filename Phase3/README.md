# Phase3 - Socket Programming Server

This project implements a simple multi-client chat server using Python's `socket` and `threading` modules. The server allows multiple clients to connect, exchange messages, and receive notifications when users join or leave the server.

## Features

- **Multi-client support**: Handles multiple clients simultaneously using threads.
- **Broadcast messaging**: Messages sent by one client are broadcast to all connected clients.
- **Join/Leave notifications**: Clients are notified when a user joins or leaves the server.
- **Username support**: Clients are required to provide a username upon connecting.

## Requirements

- Python 3.x
- Basic understanding of socket programming

## How to Run

1. **Start the Server**:
   - Navigate to the `Phase3` directory.
   - Run the `server.py` file:
     ```bash
     python server.py
     ```
   - The server will start listening for incoming connections.

2. **Connect Clients**:
   - Use a client program to connect to the server (e.g., a Python client script or a socket testing tool).
   - Provide a username when prompted.

3. **Send Messages**:
   - Type and send messages to broadcast them to all connected clients.
   - Type `/exit` to disconnect from the server.

## Server Details

- **Host**: The server binds to the local machine's hostname.
- **Port**: 12345

## Example Output

### Server Console
```
******************************
Server is listening for connections...
******************************
('192.168.1.2', 54321) has connected.
******************************
Client: Alice ('192.168.1.2', 54321)
******************************
Alice has joined the server.
```

### Client Console
```
Welcome Alice, you are connected to the server.

Bob: Hello everyone!
Alice: Hi Bob!
```

## Notes

- Ensure the port `12345` is not blocked by a firewall.
- The server does not currently support encryption (e.g., SSL/TLS).

## License

This project is for educational purposes and is not licensed for commercial use.