from typing import List
from copy import deepcopy


class Message:
    def __init__(
        self,
        sender: str = "",
        house: str = "",
        room: str = "",
        text: str = "",
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

    def take_recipients(self) -> List[str]:
        reciepents = self.reciepents
        self.reciepents = []
        return reciepents

    def convert(
        self,
        action: str = "normal",
        text: str = "",
        house: str = "",
        room: str = "",
        reciepents: list[str] = [],
    ) -> "Message":
        message = self.clone()
        message.reciepents = reciepents if reciepents else [message.sender]
        message.action = action
        if room:
            message.room = room
        if house:
            message.house = house
        if text:
            message.text = text

        print(message, message.action)
        return message

    def __repr__(self):
        return f"sender: {self.sender}\nhouse: {self.house}\nroom: {self.room}\ntext: {self.text}"

    def __str__(self):
        return f"sender: {self.sender}\nhouse: {self.house}\nroom: {self.room}\ntext: {self.text}"
