# Phase4 - Chat Application with PyQt6

This project implements a graphical chat client using Python's `PyQt6` for the user interface and `socket` for network communication. The client connects to a chat server, allowing users to send and receive messages in real time.

## Features

- **Graphical User Interface (GUI)**: Built with PyQt6 for a modern and user-friendly experience.
- **Multi-client support**: Connects to a server that supports multiple clients.
- **Customizable text color**: Users can select their preferred text color for messages.
- **Join/Leave notifications**: Users are notified when someone joins or leaves the chat.
- **Private messaging**: Supports private messages with a distinct style.

## Requirements

- Python 3.x
- PyQt6 library
- A running chat server (e.g., the server implemented in Phase3)

## How to Run

1. **Install Dependencies**:
   - Install PyQt6 using pip:
     ```bash
     pip install PyQt6
     ```

2. **Start the Server**:
   - Ensure the chat server is running (e.g., the server from Phase3).

3. **Run the Client**:
   - Navigate to the `Phase4` directory.
   - Run the `clint.py` file:
     ```bash
     python clint.py
     ```

4. **Connect to the Server**:
   - Enter the server IP, port, and your username in the connection settings.
   - Select your preferred text color.
   - Click the "Connect" button to join the chat.

5. **Send Messages**:
   - Type your message in the input field and press "Send" or hit Enter.
   - To disconnect, click the "Disconnect" button.

## Application Details

- **Server IP**: Defaults to the local machine's IP address.
- **Port**: Defaults to `12345`.
- **Username**: Required to identify the user in the chat.

## Example Screenshots

### Connection Settings
- Enter server details, username, and select text color.

### Chat Window
- View messages from all users in the chat.

## Notes

- Ensure the server IP and port match the running server.
- The application does not currently support encryption (e.g., SSL/TLS).

## License

This project is for educational purposes and is not licensed for commercial use.