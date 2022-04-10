from typing import List, Any
from copy import deepcopy


class Message:
    """
    A message class for tranferring data between server and client
    """

    def __init__(
        self,
        sender: str = "SERVER",
        house: str = "",
        room: str = "",
        text: str = "",
        action: str = "",
        reciepents: List[str] = [],
        data: dict[str, Any] = {},
    ):
        self.action = action
        self.sender = sender
        self.house = house
        self.room = room
        self.text = text
        self.reciepents = reciepents
        self.data = data

    def clone(self) -> "Message":
        return deepcopy(self)

    def take_recipients(self) -> List[str]:
        """
        Takes the ownership of reciepents and replace it with
        a empty list to reduce message load
        """

        reciepents = self.reciepents
        self.reciepents = []
        return reciepents

    def convert(
        self,
        sender: str = "SERVER",
        action: str = "push_text",
        text: str = "",
        house: str = "",
        room: str = "",
        reciepents: list[str] = [],
        data: dict[str, str] = {},
    ) -> "Message":
        """
        Converts some parts of the message for different actions
        """

        message = self.clone()
        message.reciepents = reciepents if reciepents else [message.sender]
        message.action = action
        if room:
            message.room = room
        if house:
            message.house = house
        if text:
            message.text = text
        if sender == "SERVER":
            message.sender = "SERVER"

        message.data = data

        return message
