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

    def add_chat(self, user: str):
        if user not in self.home.rooms:
            self.send(Message(action="add_room", house="HOME", text=user))
            self.home.add_room(user)

    def clear_chat(self, name: str):
        self.send(Message(action="clear_chat", house="HOME", text=name))

    def add_house(self, name: str):
        self.houses.add(name)
        self.send(Message(action="add_house", text=name))

    def del_house(self, name: str):
        self.houses.remove(name)
        self.send(Message(action="del_house", text=name))

    def add_room(self, house: str, room: str):
        self.send(Message(action="add_room", house=house, room=room))

    def del_room(self, house: str, room: str):
        self.send(Message(action="del_room", house=house, room=room))

    def add_rank(self, house: str, rank: str):
        self.send(Message(action="add_rank", house=house, text=rank))

    def del_rank(self, house: str, rank: str):
        self.send(Message(action="del_rank", house=house, text=rank))

    def del_user_rank(self, house: str, rank: str, user: str):
        self.send(
            Message(
                action="del_user_rank", house=house, data={"rank": rank, "user": user}
            )
        )

    def add_user_rank(self, house: str, rank: str, user: str):
        self.send(
            Message(
                action="add_user_rank", house=house, data={"rank": rank, "user": user}
            )
        )

    def silent_user(self, user: str):
        self.home.muted_users.add(user)

    def unsilent_user(self, user: str):
        self.home.muted_users.remove(user)
