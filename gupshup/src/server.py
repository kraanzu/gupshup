import socket
from time import sleep
from threading import Thread
from typing import Dict, List
from .utils import Message, House, User

HOST = "localhost"
PORT = 5500


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))

        self.users: Dict[str, User] = dict()
        self.houses: Dict[str, House] = dict()

    def broadcast(self, message: Message, reciepents: List[str]):
        if message.house != "HOME" and message.sender != "SERVER":
            house = self.houses[message.house]
            color = house.ranks[house.member_rank[message.sender]].color
        elif message.sender == "SERVER":
            color = "red"
        else:
            color = "magenta"

        message.sender = f"[{color}]{message.sender}[/{color}]"

        for user in reciepents:
            self.users[user].send(message)

        # TODO: modify `Channel` class so that this sleep is not needed
        sleep(0.1)

    # +-------------------------------+
    # | Methods to manage user data   |
    # | When sent from `HOME`         |
    # +-------------------------------+

    def action_join(self, message: Message):
        house = message.text[6:]
        if house not in self.houses:
            return [message.convert(text="No such house")]

        return self.houses[house].process_message(message)

    def action_add_room(self, message) -> List[Message]:
        param = message.text[10:].strip()

        if param == message.sender:
            return [
                message.convert(
                    text="If you really are that alone that you want to talk with yourself.."
                    + "\nyou can shoot lame messages in the general section of this house ",
                )
            ]

        if param not in self.users:
            return [
                message.convert(
                    text="No user with such name!",
                ),
            ]
        else:
            if self.users[param].has_banned(message.sender):
                return [
                    message.convert(
                        text="This user has blocked you so you can't connect",
                    )
                ]
            else:
                self.users[message.sender].add_chat(param)
                return [
                    message.convert(action="add_room", text=param),
                    message.convert(
                        text="You can now chat with the user",
                    ),
                ]

    def action_add_house(self, message):
        param = message.text[11:]
        if param in self.houses:
            return [
                message.convert(
                    text="There is already a house with same name",
                )
            ]
        else:
            message.house = param
            self.houses[param] = House(param, message.sender)
            return [
                message.convert(
                    action="add_house",
                    data={"house": self.houses[param]._generate_house_data()},
                )
            ]

    def action_ban(self, message):
        param = message.text[5:]
        if param not in self.users:
            return [
                message.convert(
                    text="No user with such name!",
                ),
            ]
        else:
            self.users[message.sender].ban_user(param)
            return [
                message.convert(
                    text=f"User `{param}` can't send you private texts now",
                )
            ]

    def action_silent(self, message: Message) -> List[Message]:
        param = message.text[8:]
        if param not in self.users:
            return [
                message.convert(
                    text="No user with such name!",
                ),
            ]
        else:
            self.users[message.sender].silent_user(param)
            return [
                message.convert(
                    text=f"messages from `{param}` won't have a notification ring now",
                )
            ]

    def action_del_chat(self, message: Message) -> List[Message]:
        if message.room == "general":
            return [message.convert(action="del_chat")]

        return [message.convert(action="del_room")]

    # ----------------------- END OF HOME FUNCTIONS ---------------------------------

    def handle_user_message(self, message: Message) -> List[Message]:
        text = message.text
        if message.room == "general" and text[0] in "/":
            try:
                action, *_ = text[1:].split(" ", 1)
                cmd = f"self.action_{action}(message)"
                return eval(cmd)

            except AttributeError:
                return [
                    message.convert(
                        text="[red]No such command! See help menu by pressing ctrl-h[/red]",
                    )
                ]

            except ValueError:
                return [
                    message.convert(
                        text="[red]invalid usage of parameters! Press ctrl+h for help menu[/red]",
                    )
                ]
        else:
            if message.room == "general":
                return [message.convert(sender="self")]
            else:
                if self.users[message.room].has_banned(message.sender):
                    return [message.convert(sender="self")]

                self.users[message.room].add_chat(message.sender)
                return [
                    message.convert(
                        sender="self", room=message.sender, reciepents=[message.room]
                    ),
                    message.convert(sender="self"),
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
