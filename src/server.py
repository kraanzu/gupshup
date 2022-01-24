import socket
from threading import Thread
from typing import Dict
from .utils import Channel

HOST = "localhost"
PORT = 5500


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.users: Dict[str, Channel] = dict()

    def serve_user(self, user: str):
        channel = self.users[user]
        while True:
            try:
                message = channel.recv()
                print(f"recved {message}")
                channel.send(f"You sent: {message}")
            except:
                print("USER Discnted")
                return

    def start_connection(self):
        self.server.listen()
        print("[+]", "server is up and running")
        while True:
            conn, addr = self.server.accept()
            self.users["test"] = Channel(conn)
            print(f"{addr} joined")
            Thread(target=self.serve_user, args=("test",), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start_connection()
