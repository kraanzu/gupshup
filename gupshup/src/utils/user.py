from socket import socket
from .channel import Channel
from .message import Message
from .house import House


class User:
    """
    A user class to make interaction with user data a bit less messy
    """

    def __init__(self, username: str, conn: socket):
        self.username = username
        self.channel = Channel(conn)
        self.home = House("HOME", self.username)
        self.houses = set()

    def close(self):
        self.channel.conn.close()

    def send(self, message: Message):
        self.channel.send(message)

    def recv(self):
        return self.channel.recv()

    def has_banned(self, user):
        return user in self.home.banned_users

    def has_joined(self, house: str):
        return house in self.houses

    def has_silent(self, user):
        return user in self.home.muted_users

    def ban_user(self, user: str):
        self.home.ban_user(user)

    def unban_user(self, user: str):
        self.home.banned_users.remove(user)
