import os
import socket
from sys import argv
from threading import Thread
from queue import Queue
from time import sleep
from pickle import load, dump

from .utils import Message, Channel

HOST = "localhost"
PORT = 5500
HOME = os.path.expanduser("~")
GUPSHUP_FOLDER = os.path.join(HOME, ".gupshup")
CHAT_DATA = os.path.join(GUPSHUP_FOLDER, argv[1])


class Client:
    def __init__(self, name: str, message_queue: Queue = Queue()) -> None:
        self.name = argv[1]
        self.queue = message_queue
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online = True
        self.setup_db()

    def setup_db(self) -> None:
        """
        Reads if an offline data is present,
        if yes, then loads the offline data
        """

        try:
            os.mkdir(GUPSHUP_FOLDER)
        except:
            pass

        try:
            with open(CHAT_DATA, "rb") as f:
                self.chats = load(f)
        except:
            self.chats = []
            with open(CHAT_DATA, "wb") as f:
                dump(self.chats, f)

        self.start = len(self.chats)

    def save_chats(self) -> None:
        """
        Save the chats before closing the application
        """
        with open(CHAT_DATA, "wb") as f:
            dump(self.chats, f)

    def send(self, message: Message) -> None:
        try:
            self.channel.send(message)
        except:
            self.try_reconnect()

    def listen_from_server(self) -> None:
        """
        Listens from server and add the messages to a working Queue
        """
        while 1:
            try:
                data = self.channel.recv()
                self.queue.put(data)
                self.chats += (data,)
            except:
                self.queue.put(Message(action="connection_disable"))
                while not self.try_reconnect():
                    pass
                self.queue.put(Message(action="connection_enable"))

    def try_reconnect(self):
        """
        Try reconnect on a connection failure
        """

        try:
            self.conn.connect((HOST, PORT))
            self.conn.sendall(self.name.encode())
            self.channel = Channel(self.conn)
            sleep(0.2)
            self.conn.sendall("-1".encode())
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
            sleep(0.2)  # A mild delay for non-mangled recieve

            self.conn.sendall(str(self.start).encode())
            self.channel = Channel(self.conn)
            Thread(target=self.listen_from_server, daemon=True).start()
        except:
            print("Looks like the server is down :(")
            exit()
