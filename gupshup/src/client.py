import os
import socket
from threading import Thread
from queue import Queue
from time import sleep
from pickle import load, dump

from .utils import Message, Channel

HOST = "localhost"
PORT = 5500
HOME = os.path.expanduser("~")


class Client:
    def __init__(self, name: str, message_queue: Queue = Queue()) -> None:
        self.name = name
        self.queue = message_queue
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online = True
        self.GUPSHUP_FOLDER = os.path.join(HOME, ".config", "gupshup")
        self.CHAT_DATA = os.path.join(self.GUPSHUP_FOLDER, self.name)
        self.setup_db()

    def setup_db(self) -> None:
        """
        Reads if an offline data is present,
        if yes, then loads the offline data
        """

        try:
            os.mkdir(self.GUPSHUP_FOLDER)
        except FileExistsError:
            pass

        try:
            with open(self.CHAT_DATA, "rb") as f:
                self.chats = load(f)
        except FileNotFoundError:
            self.chats = []
            with open(self.CHAT_DATA, "wb") as f:
                dump(self.chats, f)

        self.start = len(self.chats)

    def save_chats(self) -> None:
        """
        Save the chats before closing the application
        """
        with open(self.CHAT_DATA, "wb") as f:
            dump(self.chats, f)

    def send(self, message: Message) -> None:
        try:
            self.channel.send(message)
        except BrokenPipeError:
            self.try_reconnect()

    def close_connection(self):
        self.conn.close()
        # self.channel.close()

    def listen_from_server(self) -> None:
        """
        Listens from server and add the messages to a working Queue
        """
        while 1:
            try:
                data = self.channel.recv()
                self.queue.put(data)
                self.chats += (data,)
            except EOFError:
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
            self.channel.close()

            self.channel = Channel(self.conn)
            sleep(0.01)
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
            sleep(0.01)  # A mild delay for non-mangled recieve

            self.conn.sendall(str(self.start).encode())
            self.channel = Channel(self.conn)
            Thread(target=self.listen_from_server, daemon=True).start()

        except ConnectionRefusedError:
            print("Looks like the server is down :(")
            exit()
