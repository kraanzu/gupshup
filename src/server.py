import socket
from time import sleep
from threading import Thread
from typing import Dict, List
from .utils import Channel, Message, House, User
from collections import defaultdict

HOST = "localhost"
PORT = 5500


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.users: Dict[str, User] = dict()
        self.user_bans: Dict[str, list] = defaultdict(list)
        self.houses: Dict[str, House] = dict()

    def broadcast(self, message: Message, reciepents: List[str]):

        for user in reciepents:
            self.users[user].send(message)

        # TODO: modify `Channel` class so that this sleep is not needed
        sleep(0.1)

    def action_add_room(self, message) -> List[Message]:
        param = message.text[10:].strip()
        print('X', param, message.sender)

        if param == message.sender:
            return [
                message.convert(
                    action="warn",
                    text="If you really are that alone that you want to talk with yourself.."
                    + "\nyou can shoot lame messages in the general section of this house ",
                )
            ]

        if param not in self.users:
            return [
                message.convert(
                    action="warn",
                    text="No user with such name!",
                ),
            ]
        else:
            if self.users[param].has_banned(message.sender):
                return [
                    message.convert(
                        action="warn",
                        text="This user has blocked you so you can't connect",
                    )
                ]
            else:
                self.users[message.sender].add_user(param)
                return [
                    message.convert(
                        action="success",
                        text="You can now chat with the user",
                    ),
                ]

    def action_add_house(self, message):
        param = message.text[11:]
        if param in self.houses:
            return [
                message.convert(
                    action="warn",
                    text="There is already a house with same name",
                )
            ]
        else:
            self.houses[param] = House(param, message.sender)
            return [
                message.convert(action="add_house", text=param),
                message.convert(
                    action="success",
                    text="Your new house is ready to rock!",
                ),
            ]

    def action_ban(self, message):
        param = message.text[5:]
        if param not in self.users:
            return [
                message.convert(
                    action="warn",
                    text="No user with such name!",
                ),
            ]
        else:
            self.users[message.sender].ban_user(param)
            return [
                message.convert(
                    action="success",
                    text=f"User `{param}` can't send you private texts now",
                )
            ]

    def handle_user_message(self, message: Message) -> List[Message]:
        text = message.text
        if message.room == "general" and text[0] in "?/":
            action, _ = text[1:].split(" ", 1)
            try:
                cmd = f"self.action_{action}(message)"
                print(cmd)
                return eval(cmd)
            except:
                return [
                    message.convert(
                        action="warn",
                        text="No such command! See help menu by pressing ctrl-h",
                    )
                ]
        else:
            if message.room == "general":
                return [message.convert()]
            else:
                if self.users[message.room].has_banned(message.sender):
                    return [message.convert()]

                self.users[message.room].add_user(message.sender)
                return [
                    message.convert(room=message.sender, reciepents=[message.room]),
                    message.convert(),
                ]

    def serve_user(self, user: str):
        while True:
            try:
                message = self.users[user].recv()
                if message.house == "HOME":
                    message_list = self.handle_user_message(message)
                    for message in message_list:
                        recipients = message.take_recipients()
                        self.broadcast(message, recipients)
                else:
                    message_list = self.houses[message.house].process_message(message)
                    for message in message_list:
                        recipients = message.take_recipients()
                        self.broadcast(message, recipients)

            except Exception as e:
                print(e)
                return

    def start_connection(self):
        self.server.listen()
        print("[+]", "server is up and running")
        while True:
            conn, _ = self.server.accept()
            username = conn.recv(1024).decode()

            self.users[username] = User(username, conn)
            self.houses[username] = House(username, username)
            print(f"{username} joined")
            Thread(target=self.serve_user, args=(username,), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start_connection()
