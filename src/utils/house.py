from typing import Dict, List
from .message import Message
from .rank import Rank
from collections import defaultdict


class House:
    def __init__(self, name: str, king: str):
        self.name = name
        self.king = king
        self.rooms = {"general"}
        self.members = [king]
        self.banned_users = set()
        self.muted_users = []
        self.bot_binds = []
        self.member_rank: Dict[str, str] = {king: "king"}
        self.ranks: Dict[str, Rank] = {"king": Rank("king")}
        self.power_levels: Dict[str, float] = {"king": float("inf")}
        self.required_power: Dict[str, float] = defaultdict(lambda: float("inf"))

    def _is_allowed(self, action: str, user: str) -> bool:
        return self.power_levels[self.member_rank[user]] >= self.required_power[action]

    def process_special_message(self, message: Message) -> List[Message]:
        action, param = message.text[1:].split(" ", 1)
        match action:
            case "addroom":
                if self._is_allowed("addroom", message.sender):
                    if param not in self.rooms:
                        action_message = message.clone()
                        action_message.action = "add_room"
                        action_message.text = param
                        action_message.reciepents = self.members

                        message.action = "push_text"
                        message.text = f"{message.sender} added a new room `{param}`"
                        message.sender = "SERVER"
                        message.reciepents = self.members
                        return [action_message, message]
                else:
                    message.action = "warn"
                    message.text = "The room with same name is already present"
                    message.reciepents = [message.sender]
                    message.sender = "SERVER"
                    return [message]

        return [message]

    def process_message(self, message: Message) -> List[Message]:
        text = message.text
        if text[0] == "/":
            return self.process_special_message(message)

        message.action = "push_text"
        message.reciepents = self.members
        return [message]

    def add_room(self, name: str) -> None:
        self.rooms.add(name)

    def del_room(self, name: str) -> None:
        self.rooms.remove(name)

    def ban_user(self, name: str) -> None:
        self.banned_users.add(name)
