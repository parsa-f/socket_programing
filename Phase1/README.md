# Phase 1: Single-Client Chat Server

## Overview
This project implements a basic single-client chat server using Python's `socket` module. The server allows one client to connect, exchange messages, and gracefully handle disconnections.

## Features
- Single-client support.
- Interactive communication between the server and the client.
- Graceful handling of client disconnections.
- Server shutdown with a clean exit.

## Requirements
- Python 3.x
- `termcolor` library for colored terminal output.

## Installation
1. Install the required library:
   ```bash
   pip install termcolor
   ```

## How to Run
1. Navigate to the `Phase1` directory:
   ```bash
   cd "c:\Users\Parsa\Desktop\socket programing\Phase1"
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Connect a client using a socket client (e.g., Telnet or a custom client script).

## Server Commands
- `/exit`: Disconnect the client or shut down the server.

## File Structure
- `server.py`: The main server script.
- `README.md`: Documentation for the project.

## Notes
- The server listens on `0.0.0.0:12345` by default. Modify the `server.py` file to change the host or port if needed.
- Only one client can connect at a time in this phase.

## Future Improvements
- Add support for multiple clients.
- Implement a more robust protocol for communication.
- Add encryption for secure communication.
