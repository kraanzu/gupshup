from typing import Dict, List, Literal
from .message import Message
from .rank import Rank
from collections import defaultdict


class House:
    def __init__(self, name: str, king: str) -> None:
        self.type = "private"
        self.name = name
        self.king = king
        self.rooms = {"general"}
        self.members = {king}
        self.banned_users = set()
        self.muted_users = set()
        self.bot_binds = set()
        self.waiting_users = set()
        self.member_rank: Dict[str, str] = {king: "king"}
        self.ranks: Dict[str, Rank] = {
            "king": Rank("king", "red", float("inf")),
            "pawn": Rank("pawn"),
        }
        self.power_levels: Dict[str, float] = {"king": float("inf")}
        self.required_power: Dict[str, float] = defaultdict(lambda: float("inf"))

    def _is_allowed(self, action: str, user: str) -> bool:
        return self.power_levels[self.member_rank[user]] >= self.required_power[action]

    def add_member(self, user: str) -> List[Message]:
        self.members.add(user)
        self.member_rank[user] = "pawn"
        return [
            Message(
                sender="SERVER",
                house="HOME",
                room="general",
                text=f"Yay now you are a part of the house `{self.name}` !",
                reciepents=[user],
            ),
            Message(action="add_house", text=self.name, reciepents=[user]),
            *[
                Message(
                    action="add_room", house=self.name, text=room, reciepents=[user]
                )
                for room in self.rooms
                if room != "general"
            ],
            Message(
                action="info",
                house=self.name,
                room="general",
                text=f"A wild {user} appeared!",
                reciepents=list(self.members),
            ),
        ]

    def action_change_type(self, _: Message) -> List[Message]:
        self.type = "open" if self.type == "private" else "private"
        for user in self.waiting_users:
            self.add_member(user)
        self.waiting_users = set()

        return [
            Message(
                action="info",
                house=self.name,
                room="general",
                text=f"The group changed its type to {self.type}",
                reciepents=list(self.members),
            )
        ]

    def add_to_waiting_list(self, user: str):
        self.waiting_users.add(user)

    def action_join(self, message: Message) -> List[Message]:
        print("JOIN OK")
        if self.type == "open":
            return self.add_member(message.sender)

        self.add_to_waiting_list(message.sender),
        return [
            message.convert(
                action="info",
                text="Your request has been sent to the king of the house",
            ),
            Message(
                sender="SERVER",
                house=self.name,
                room="general",
                text=f"User {message.sender} has requested to join the group",
                reciepents=[self.king],
            ),
        ]

    def action_add_room(self, message: Message) -> List[Message]:
        if not self._is_allowed("add_room", message.sender):
            return [
                message.convert(
                    action="warn",
                    text="Your current power level doesn't allow this action",
                )
            ]

        room = message.text[10:]
        if room in self.rooms:
            return [
                message.convert(
                    action="warn", text="There is already a room with same name!"
                )
            ]

        self.add_room(room)
        return [
            message.convert(action="add_room", text=room, reciepents=list(self.members))
        ]

    def action_accept(self, message: Message) -> List[Message]:
        user = message.text[8:].strip()
        if user not in self.waiting_users:
            return [
                Message(
                    action="warn",
                    house=self.name,
                    room="general",
                    text=f"no such user({user}) in the waiting list",
                    reciepents=[self.king],
                ),
            ]

        return self.add_member(user)

    def process_special_message(self, message: Message) -> List[Message]:
        action, _ = message.text[1:].split(" ", 1)
        cmd = f"self.action_{action}(message)"
        print("special", cmd)
        return eval(cmd)

    def process_message(self, message: Message) -> List[Message]:
        print("process_message OK")
        text = message.text
        if text[0] == "/":
            return self.process_special_message(message)

        return [message.convert(reciepents=list(self.members))]

    def add_room(self, name: str) -> None:
        self.rooms.add(name)

    def del_room(self, name: str) -> None:
        self.rooms.remove(name)

    def ban_user(self, name: str) -> None:
        self.banned_users.add(name)
