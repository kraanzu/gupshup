from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget


class Banner(Widget):
    """
    A Banner widget to show the current house/group
    """

    text = Text("HOME/general", style="bold blue")

    def set_text(self, text: str):
        self.text = Text(text, style="bold blue")
        self.refresh()

    def render(self) -> RenderableType:
        return Panel(Align.center(self.text))
