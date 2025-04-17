import socket
import time
from termcolor import colored

def start_client():
    # Client configuration
    SERVER_IP = '127.0.0.1'  # Use 'localhost' or the server's exact IP
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024

    try:
        # Create and connect socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))
        
        print(colored(f"Connected to server at {SERVER_IP}:{SERVER_PORT}", "green"))
        
        # Receive welcome message
        welcome_msg = sock.recv(BUFFER_SIZE).decode('utf-8')
        print(colored(welcome_msg.strip(), "blue"))

        # Chat loop
        while True:
            try:
                # Get user input
                message = input(colored("You: ", "yellow"))
                sock.send(message.encode('utf-8'))
                
                if message.lower() == "/exit":
                    print(colored("Disconnecting...", "red"))
                    break
                
                # Receive server response
                response = sock.recv(BUFFER_SIZE).decode('utf-8')
                if not response:  # Server closed connection
                    print(colored("Server disconnected", "red"))
                    break
                    
                if response.lower() == "/exit":
                    print(colored("Server closed the connection", "red"))
                    break
                    
                print(colored(f"Server: {response}", "green"))

            except KeyboardInterrupt:
                print(colored("\nManual interrupt - disconnecting", "red"))
                sock.send("/exit".encode('utf-8'))
                break

    except ConnectionRefusedError:
        print(colored("Error: Server is not available", "red"))
    except Exception as e:
        print(colored(f"Connection error: {e}", "red"))
    finally:
        sock.close()
        print(colored("Connection closed", "blue"))

if __name__ == "__main__":
    start_client()