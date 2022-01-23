from textual.widgets import Header
from textual import events


class Headbar(Header):
    def __init__(self):
        super().__init__(tall=False, style="#88c0d0 on #3b4252")

    def watch_tall(self, _: bool) -> None:
        self.tall = False
        self.layout_size = 1

    def on_click(self, _: events.Click) -> None:
        self.tall = False
