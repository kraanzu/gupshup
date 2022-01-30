from textual.widget import Widget

from rich.console import RenderableType

from src.utils import Message

import logging

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class ChatScreen(Widget):
    def __init__(self, name: str | None = None):
        super().__init__(name)
        self.chats = ""

    def set_current_screen(self, name):
        self.current_screen = name

    def render(self) -> RenderableType:
        return self.chats

    def push_text(self, msg: Message) -> None:
        color = "red" if msg.sender == "SERVER" else "magenta"
        self.chats += f"\n[{color}]{msg.sender}[/{color}]: {msg.text}"
        self.refresh()
