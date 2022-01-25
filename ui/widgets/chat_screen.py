from textual.widget import Widget

from rich.console import RenderableType
from rich.panel import Panel

from collections import defaultdict

import logging

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class ChatScreen(Widget):

    def __init__(self, name: str | None = None):
        super().__init__(name)
        self.screens = defaultdict(str)
        self.current_screen = ''

    def set_current_screen(self, name):
        self.current_screen = name

    def render(self) -> RenderableType:
        return Panel(self.screens[self.current_screen])

    def push_text(self, screen: str, msg: str) -> None:
        self.screens[screen] += "\n" + msg
        self.refresh()
