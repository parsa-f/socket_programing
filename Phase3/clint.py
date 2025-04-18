import socket
import threading

# Create client socket (IPv4 and TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345))


def request_and_send_username():
    """Handle username request from server and send username"""
    server_message = client_socket.recv(1024).decode("utf-8")
    if server_message == "username":
        print("Please enter your username: ", end="")
        username = input()
        client_socket.send(username.encode("utf-8"))
        return 0


def handle_outgoing_messages():
    """Send messages to server"""
    while True:
        message = input("")
        if message == "/exit":
            client_socket.close()
            break
        client_socket.send(message.encode("utf-8"))


def handle_incoming_messages():
    """Receive and display messages from server"""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Disconnected!", end="")
            client_socket.close()
            break


# Create and start threads for message handling
message_receiver_thread = threading.Thread(target=handle_incoming_messages)
message_sender_thread = threading.Thread(target=handle_outgoing_messages)

# Start the communication process
request_and_send_username()
message_receiver_thread.start()
message_sender_thread.start()