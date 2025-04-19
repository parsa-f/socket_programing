# -*- coding: utf-8 -*-
import socket
import threading

class ChatServer:
    def __init__(self):
        self.clients = []
        self.nicknames = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 12345))
        self.server.listen()
        print("[*] Server started on port 12345")

    def broadcast(self, message, sender=None):
        """Send message to all clients except sender"""
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)

    def handle_client(self, client):
        """Manage individual client connections"""
        try:
            # Get nickname
            client.send("Nick Name ".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"[+] {nickname} joined the chat")
            self.broadcast(f"{nickname} joined the chat!")
            
            # Chat loop
            while True:
                message = client.recv(1024).decode('utf-8')
                if message.lower() == '/exit':
                    break
                self.broadcast(f"{nickname}: {message}", sender=client)
                
        except:
            pass
        finally:
            self.remove_client(client, nickname)

    def remove_client(self, client, nickname):
        """Clean up disconnected clients"""
        if client in self.clients:
            self.clients.remove(client)
            client.close()
        if nickname in self.nicknames:
            print(f"[-] {nickname} left")
            self.broadcast(f"{nickname} left the chat")
            self.nicknames.remove(nickname)

    def start(self):
        """Main server loop"""
        try:
            while True:
                client, addr = self.server.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(client,),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server...")
            self.broadcast("Server is shutting down!")
            for client in self.clients:
                client.close()
        finally:
            self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()