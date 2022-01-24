from textual.widget import Widget

from rich.console import RenderableType
from rich.panel import Panel

from queue import Queue

import logging

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class ChatScreen(Widget):
    chats = ""

    def __init__(self, name: str | None = None, queue: Queue = Queue()):
        self.queue = queue
        super().__init__(name)

    def render(self) -> RenderableType:
        return Panel(self.chats)

    def push_text(self, msg: str) -> None:
        self.chats += "\n-x-\n" + msg
        self.refresh()
