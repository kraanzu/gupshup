from typing import List


class Message:
    def __init__(
        self,
        sender: str,
        house: str,
        room: str,
        text: str,
        command: str = "",
        reciepents: List[str] = [],
    ):
        self.command = command
        self.command = None
        self.sender = sender
        self.house = house
        self.room = room
        self.text = text
        self.reciepents = reciepents

    def __str__(self):
        return f"\nsender: {self.sender}\nhouse: {self.house}\nroom: {self.room}\ntext: {self.text}"
