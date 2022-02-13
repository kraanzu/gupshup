import socket
from threading import Thread
from queue import Queue

from .utils import Message, Channel

HOST = "localhost"
PORT = 5500


class Client:
    def __init__(self, name: str, message_queue: Queue = Queue()):
        self.name = name
        self.queue = message_queue
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online = True

    def send(self, message: Message):
        try:
            self.channel.send(message)
        except:
            self.try_reconnect()

    def listen_from_server(self):
        while 1:
            try:
                data = self.channel.recv()
                self.queue.put(data)
            except:
                self.queue.put(Message(action="connection_disable"))
                while not self.try_reconnect():
                    pass

                self.queue.put(Message(action="connection_enable"))

    def try_reconnect(self):
        try:
            self.conn.connect((HOST, PORT))
            self.conn.sendall(self.name.encode())
            self.channel = Channel(self.conn)
            return True

        except ConnectionRefusedError:
            return False

        except OSError:
            self.conn.close()
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False

    def start_connection(self):
        try:
            self.conn.connect((HOST, PORT))
            self.conn.sendall(self.name.encode())
            self.channel = Channel(self.conn)
            Thread(target=self.listen_from_server, daemon=True).start()
        except:
            print("Looks like the server is down :(")
            exit()
