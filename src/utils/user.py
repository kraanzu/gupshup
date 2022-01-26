from socket import socket
from .channel import Channel
from .message import Message
from .house import House


class User:
    def __init__(self, username: str, conn: socket):
        self.username = username
        self.channel = Channel(conn)
        self.home = House("HOME", self.username)

    def ban_user(self, user: str):
        self.home.ban_user(user)

    def has_banned(self, user):
        return user in self.home.banned_users

    def add_user(self, user: str):
        if user not in self.home.rooms:
            self.send(Message(action="add_room", house="HOME", text=user))
            self.home.add_room(user)

    def recv(self):
        return self.channel.recv()

    def send(self, message: Message):
        self.channel.send(message)
