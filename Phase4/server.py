import socket
import threading
from datetime import datetime

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))
server_socket.listen()

# Client management dictionaries
connected_clients = {}  # socket: username
username_socket_mapping = {}  # username: socket


def get_current_clients_list():
    """Return formatted string of currently connected clients."""
    return "\n".join([f"{name}" for _, name in connected_clients.items()])


def broadcast_message_to_all(message_content):
    """
    Send a message to all connected clients.
    """
    for client_connection in connected_clients.keys():
        try:
            client_connection.send(message_content)
        except:
            connected_clients.pop(client_connection)


def handle_client_communication(client_connection):
    """
    Handle continuous communication with a connected client.
    """
    while True:
        client_address = str(client_connection)[-26:-3]
        try:
            received_message = client_connection.recv(1024).decode("utf-8")

            if received_message.startswith("/pm "):
                message_parts = received_message.split(" ", 2)
                if len(message_parts) == 3:
                    recipient_username, private_message = message_parts[1], message_parts[2]
                    sender_username = connected_clients[client_connection]

                    if recipient_username in username_socket_mapping:
                        recipient_socket = username_socket_mapping[recipient_username]
                        recipient_socket.send(
                            f"[PM from {sender_username}] {private_message}".encode("utf-8")
                        )
                        client_connection.send(f'{sender_username}: {private_message} ({datetime.now().strftime("%H:%M")})'.encode("utf-8"))
                    else:
                        client_connection.send(f"User '{recipient_username}' not found.".encode("utf-8"))
                continue

            if received_message.lower() == "/exit":
                raise Exception

            client_username = connected_clients[client_connection]
            formatted_chat_message = f"{client_username}|{received_message}"
            broadcast_message_to_all(formatted_chat_message.encode("utf-8"))

        except:
            if client_connection in connected_clients:
                client_username = connected_clients[client_connection]
                connected_clients.pop(client_connection)
                client_connection.close()
                broadcast_message_to_all(f"{client_username}|has left the server".encode("utf-8"))
                print(f"{client_username} ({client_address}) has left the server.")
                print("*" * 30)
                print(get_current_clients_list())
                print("*" * 30)
            break


def accept_client_connections():
    """
    Continuously accept new client connections and start communication threads.
    """
    while True:
        client_connection, client_address = server_socket.accept()
        print(f"{client_address} has connected.")
        print("*" * 30)

        try:
            client_username = client_connection.recv(1024).decode('utf-8')
            username_socket_mapping[client_username] = client_connection
            connected_clients.update({client_connection: client_username})

            print(f"client: {client_username} {str(client_connection)[-27:-1]}")
            print("*" * 30)

            client_connection.send(f"welcome {client_username}\n".encode('utf-8'))
            broadcast_message_to_all(f"{client_username}|has joined the server".encode("utf-8"))

        except:
            print(f"({str(client_connection)[-25:-2]}) has left the server.")
            print("*" * 30)
            print(get_current_clients_list())
            print("*" * 30)
            continue

        client_thread = threading.Thread(target=handle_client_communication, args=(client_connection,))
        client_thread.start()


# Server startup
print()
print("*" * 30)
print("server is looking for connection...")
print("*" * 30)

# Start accepting connections
accept_client_connections()