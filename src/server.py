import socket
from threading import Thread
from typing import Dict
from .utils import Channel, Message, House

HOST = "localhost"
PORT = 5500


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.users: Dict[str, Channel] = dict()
        self.houses: Dict[str, House] = dict()

    def broadcast(self, message: Message):
        for user in message.reciepents:
            self.users[user].send(message)

    def serve_user(self, user: str):
        channel = self.users[user]
        while True:
            try:
                message = channel.recv()
                print("recieved", message)
                data = self.houses[message.house].process_message(message)
                Thread(target=self.broadcast, args=(data,), daemon=True).start()

            except Exception as e:
                print(e)
                return

    def start_connection(self):
        self.server.listen()
        print("[+]", "server is up and running")
        while True:
            conn, addr = self.server.accept()
            self.users["test"] = Channel(conn)
            self.houses["test"] = House("test", "test")
            print(f"{addr} joined")
            Thread(target=self.serve_user, args=("test",), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start_connection()
