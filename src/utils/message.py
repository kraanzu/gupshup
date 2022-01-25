from typing import List
from copy import deepcopy


class Message:
    def __init__(
        self,
        sender: str,
        house: str,
        room: str,
        text: str,
        action: str = "",
        reciepents: List[str] = [],
    ):
        self.action = action
        self.sender = sender
        self.house = house
        self.room = room
        self.text = text
        self.reciepents = reciepents

    def clone(self) -> "Message":
        return deepcopy(self)

    def __str__(self):
        return f"sender: {self.sender}\nhouse: {self.house}\nroom: {self.room}\ntext: {self.text}"

    def __repr__(self):
        return f"sender: {self.sender}\nhouse: {self.house}\nroom: {self.room}\ntext: {self.text}"
