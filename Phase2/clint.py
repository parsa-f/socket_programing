# -*- coding: utf-8 -*-
import socket
import threading

def receive_messages(connection):
    """Handles incoming messages from server"""
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            if not message:
                print("\n[!] Connection closed by server")
                break
            print(f"{message}\n", end="")
        except:
            print("\n[!] Lost connection to server")
            break

def start_client():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('localhost', 12345))  # Auto-connect to localhost
    
    # Get nickname
    nickname = input("Enter your Nick Name: ")
    connection.send(nickname.encode('utf-8'))
    
    print(f"\nWelcome {nickname}! (Type /exit to quit)")
    
    # Start receive thread
    threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()
    
    # Message loop
    while True:
        message = input("You: ")
        connection.send(message.encode('utf-8'))
        if message.lower() == '/exit':
            connection.close()
            print("[+] Disconnected from server")
            break

if __name__ == "__main__":
    print("\n=== Chat Client ===")
    start_client()