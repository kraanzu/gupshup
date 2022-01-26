import socket
from time import sleep
from threading import Thread
from typing import Dict, List
from .utils import Channel, Message, House
from collections import defaultdict

HOST = "localhost"
PORT = 5500


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.users: Dict[str, Channel] = dict()
        self.user_bans: Dict[str, list] = defaultdict(list)
        self.houses: Dict[str, House] = dict()

    def broadcast(self, message: Message, reciepents: List[str]):

        for user in reciepents:
            self.users[user].send(message)

        # TODO: modify `Channel` class so that this sleep is not needed
        sleep(0.1)

    def handle_user_message(self, message: Message) -> List[Message]:
        text = message.text
        if text[0] in "?/":
            action, param = text[1:].split(" ", 1)
            if action == "addroom":
                if param not in self.users:
                    return [
                        message.convert(
                            action="warn",
                            text="No user with such name!",
                        ),
                    ]
                else:
                    if message.sender in self.user_bans[param]:
                        return [
                            message.convert(
                                action="warn",
                                text="This user has blocked you so you can't connect",
                            )
                        ]
                    else:
                        return [
                            message.convert(
                                action="add_room",
                                text=param,
                            ),
                            message.convert(
                                action="success",
                                text="You can now chat with the user",
                            ),
                        ]

            elif action == "addhouse":
                if param in self.houses:
                    return [
                        message.convert(
                            action="warn",
                            text="There is already a house with same name",
                        )
                    ]
                else:
                    return [
                        message.convert(action="add_house", text=param),
                        message.convert(
                            action="success",
                            text="Your new house is ready to rock!",
                        ),
                    ]
            else:
                return [message.convert(action="warn", text="No such command")]
        else:
            if message.room == "general":
                return [message.convert()]
            else:
                return [
                    message.convert(
                        action="add_room",
                        text=message.sender,
                        reciepents=[message.room],
                    ),
                    message.convert(room=message.sender, reciepents=[message.room]),
                    message.convert(),
                ]

    def serve_user(self, user: str):
        channel = self.users[user]
        while True:
            try:
                message = channel.recv()
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

            self.users[username] = Channel(conn)
            self.houses[username] = House(username, username)
            print(f"{username} joined")
            Thread(target=self.serve_user, args=(username,), daemon=True).start()


if __name__ == "__main__":
    server = Server()
    server.start_connection()
