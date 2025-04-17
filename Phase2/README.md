# Phase 2: Python Chat Server

## Overview
This project implements a simple multi-client chat server using Python's `socket` and `threading` modules. The server allows multiple clients to connect, exchange messages, and gracefully handle disconnections.

## Features
- Multi-client support using threads.
- Nickname-based identification for clients.
- Broadcast messages to all connected clients.
- Graceful handling of client disconnections.
- Server shutdown with a broadcast notification.

## Requirements
- Python 3.x
- No additional libraries are required.

## How to Run
1. Navigate to the `Phase2` directory:
   ```bash
   cd "c:\Users\Parsa\Desktop\socket programing\Phase2"
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Connect clients using a socket client (e.g., Telnet or a custom client script).

## Server Commands
- `/exit`: Disconnect a client from the server.
- Server shutdown: Use `Ctrl+C` to stop the server, which will notify all connected clients.

## File Structure
- `server.py`: The main server script.
- `README.md`: Documentation for the project.

## Notes
- Ensure the server is running before connecting clients.
- The server listens on `0.0.0.0:12345` by default. Modify the `server.py` file to change the host or port if needed.

## Future Improvements
- Add encryption for secure communication.
- Implement a GUI for the server and clients.
- Add user authentication for enhanced security.