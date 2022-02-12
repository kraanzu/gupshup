from textual.widget import Widget
from rich.console import RenderableType
from ...src.utils import Message


class ChatScreen(Widget):
    def __init__(self, name: str | None = None):
        super().__init__(name)
        self.chats = ""

    def set_current_screen(self, name):
        self.current_screen = name

    def render(self) -> RenderableType:
        return self.chats

    def push_text(self, message: Message) -> None:
        self.chats += f"\n{message.sender}: {message.text}"
        self.refresh()
