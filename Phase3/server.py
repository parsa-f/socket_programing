import socket
import threading

# Create server socket (IPv4 and TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to host and port
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# Listen for incoming connections
server_socket.listen()

# Dictionary to track connected clients
connected_clients = {}


def broadcast_message(message):
    """Send message to all connected clients"""
    for client_socket in connected_clients.keys():
        client_socket.send(message)


def handle_client_messages(client_socket):
    """Handle messages from a specific client"""
    while True:
        client_address = str(client_socket)[-26:-3]
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message.lower() == "/exit":
                raise Exception
            formatted_message = f"\033[1;34m\n\t{connected_clients[client_socket]} ({client_address}): {message}\n\033[0m".encode("utf-8")
            broadcast_message(formatted_message)
        except:
            client_name = connected_clients[client_socket]
            connected_clients.pop(client_socket)
            client_socket.close()
            leave_message = f"\033[1;31m\n\t{client_name} ({client_address}) has left the server!\n\033[0m".encode("utf-8")
            broadcast_message(leave_message)
            print(f"{client_name} ({client_address}) has left the server.")
            print("*" * 30)
            break


def manage_client_connections():
    """Handle new client connections"""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} has connected.")
        print("*" * 30)

        try:
            # Request client username
            client_socket.send(f"username".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8')

            if len(username) != 0:
                connected_clients.update({client_socket: username})
                print(f"Client: {connected_clients[client_socket]} {str(client_socket)[-27:-1]}")
                print("*" * 30)

                welcome_message = f"\nWelcome {connected_clients[client_socket]}, you are connected to the server.\n".encode('utf-8')
                client_socket.send(welcome_message)
                join_notification = f"\033[1;92m\n{connected_clients[client_socket]} has joined the server.\n\033[0m".encode("utf-8")
                broadcast_message(join_notification)
            else:
                raise Exception

        except:
            print(f"({str(client_socket)[-25:-2]}) has left the server.")
            print("*" * 30)
            continue

        client_thread = threading.Thread(target=handle_client_messages, args=(client_socket,))
        client_thread.start()


# Server startup message
print()
print("*" * 30)
print("Server is listening for connections...")
print("*" * 30)
manage_client_connections()