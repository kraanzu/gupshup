import socket
import loguru
from threading import Thread
from queue import Queue
from pickle import dumps, loads

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
        self.channel.send(message)

    # def send(self, message: str):
    #     self.channel.send(message)

    def listen_from_server(self):
        while 1:
            try:
                data = self.channel.recv()
                self.queue.put(data)
            except Exception as e:
                self.queue.put("cannnooott")

    def start_connection(self):
        try:
            self.conn.connect((HOST, PORT))
            self.conn.sendall(self.name.encode())
            self.channel = Channel(self.conn)
            Thread(target=self.listen_from_server, daemon=True).start()
        except:
            print("Looks like the server is down :(")
            exit()
