import socket
import time
from termcolor import colored

def start_server():
    # Server configuration
    HOST = '0.0.0.0'  # Listen on all available interfaces
    PORT = 12345
    BUFFER_SIZE = 1024
    MAX_CONNECTIONS = 1  # Single client mode

    server_socket = None
    client_socket = None

    try:
        # Create and configure server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS)

        print(colored(f"Server started on port {PORT}", "blue"))
        print(colored("Waiting for incoming connections...", "yellow"))

        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(colored(f"Connection established with {client_address[0]}", "green"))

        # Send welcome message
        welcome_msg = """
        ********************************
        *  Welcome to Chat Server  *
        *  Type /exit to quit  *
        ********************************
        """
        client_socket.send(welcome_msg.encode('utf-8'))

        # Main communication loop
        while True:
            try:
                # Receive message from client
                message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                
                if not message:  # Client disconnected
                    print(colored("Client disconnected", "red"))
                    break
                    
                if message.lower() == "/exit":
                    print(colored("Client requested disconnect", "yellow"))
                    client_socket.send("Server acknowledging disconnect".encode('utf-8'))
                    break
                
                print(colored(f"Client: {message}", "green"))
                
                # Get server response
                response = input(colored("Your reply: ", "yellow"))
                client_socket.send(response.encode('utf-8'))
                
                if response.lower() == "/exit":
                    print(colored("Closing connection...", "red"))
                    break

            except ConnectionResetError:
                print(colored("Client connection lost unexpectedly!", "red"))
                break
            except KeyboardInterrupt:
                print(colored("\nServer shutdown initiated", "red"))
                client_socket.send("/exit".encode('utf-8'))
                break

    except Exception as e:
        print(colored(f"Server error: {str(e)}", "red"))
    finally:
        # Clean up sockets
        if client_socket:
            client_socket.close()
        if server_socket:
            server_socket.close()
        print(colored("\nServer shutdown complete", "blue"))

if __name__ == "__main__":
    start_server()