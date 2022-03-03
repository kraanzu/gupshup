from textual.widgets import Header
from rich.table import Table
from rich.console import RenderableType
from rich.panel import Panel
from textual import events


class Headbar(Header):
    """
    Custom Header for Gupshup showing status for the server and a Welcome message
    """

    def __init__(self):
        super().__init__(
            tall=False, style="magenta on black"
        )
        self.status = " Online"

    def watch_status(self, _: str):
        self.refresh()

    def render(self) -> RenderableType:
        header_table = Table.grid(
            padding=(1, 1), expand=True
        )
        header_table.style = self.style
        header_table.add_column(
            justify="left", ratio=0, width=20
        )
        header_table.add_column(
            "title", justify="center", ratio=1
        )
        header_table.add_column(
            "clock", justify="center", width=10
        )
        header_table.add_row(
            self.status,
            self.full_title,
            self.get_clock() if self.clock else "",
        )
        header: RenderableType
        header = (
            Panel(header_table, style=self.style)
            if self.tall
            else header_table
        )
        return header

    def watch_tall(self, _: bool) -> None:
        self.tall = False
        self.layout_size = 1

    def on_click(self, _: events.Click) -> None:
        self.tall = False
