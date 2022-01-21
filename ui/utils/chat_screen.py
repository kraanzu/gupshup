import queue
from textual.widget import Widget

from rich.console import RenderableType
from rich.panel import Panel

from queue import Queue


class ChatScreen(Widget):
    chats = ""

    def __init__(self, name: str | None = None, queue: Queue = Queue()):
        self.queue = queue
        super().__init__(name)

    def on_mount(self, _):
        self.set_interval(1, self.server_listen)

    def server_listen(self):
        while self.queue.qsize():
            self.push_text(self.queue.get())

    def render(self) -> RenderableType:
        return Panel(self.chats)

    def push_text(self, msg: str):
        self.chats += "\n" + msg
        self.refresh()
