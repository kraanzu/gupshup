# thanks to textual_inputs
# https://github.com/sirfuzzalot/textual-inputs

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, Union

import rich.box
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from textual import events
from textual.reactive import Reactive
from textual.widget import Widget


if TYPE_CHECKING:
    from rich.console import RenderableType


class TextInput(Widget):
    """
    A simple text input widget.
    """

    value: Reactive[str] = Reactive("")
    cursor: str = "|"
    _cursor_position: Reactive[int] = Reactive(0)
    _has_focus: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        value: str = "",
        placeholder: str = "",
    ) -> None:
        super().__init__(name)
        self.value = value
        self.placeholder = placeholder
        self._cursor_position = len(self.value)

    @property
    def has_focus(self) -> bool:
        """Produces True if widget is focused"""
        return self._has_focus

    def render(self) -> RenderableType:
        """
        Produce a Panel object containing placeholder text or value
        and cursor.
        """
        if self.has_focus:
            text = self._render_text_with_cursor()
        else:
            if len(self.value) == 0:
                text = Text(self.placeholder, style="dim white")
            else:
                text = Text(self.value)

        return Panel(
            text,
            height=3,
            style=self.style or "",
            border_style=self.border_style or Style(color="blue"),
            box=rich.box.DOUBLE if self.has_focus else rich.box.SQUARE,
        )

    def _render_text_with_cursor(self) -> Text:
        """
        Produces the renderable Text object combining value and cursor
        """
        text = Text()
        text.append(self.value[: self._cursor_position])
        text.append(self.cursor, style="bold")
        text.append(self.value[self._cursor_position :])
        return text

    async def on_focus(self, _: events.Focus) -> None:
        self._has_focus = True

    async def on_blur(self, _: events.Blur) -> None:
        self._has_focus = False

    async def on_key(self, event: events.Key) -> None:
        if event.key == "left":
            self._cursor_position = max(self._cursor_position - 1, 0)

        elif event.key == "right":
            self._cursor_position = min(self._cursor_position + 1, len(self.value))

        elif event.key == "home":
            self._cursor_position = 0

        elif event.key == "end":
            self._cursor_position = len(self.value)

        elif event.key == "ctrl+h":  # Backspace
            if self._cursor_position:
                self._cursor_position = max(self._cursor_position - 1, 0)
                self.value = (
                    self.value[: self._cursor_position]
                    + self.value[self._cursor_position + 1 :]
                )

        elif event.key == "delete":
            self.value = (
                self.value[: self._cursor_position]
                + self.value[self._cursor_position + 1 :]
            )

        elif event.key != "enter":
            self.value = (
                self.value[: self._cursor_position]
                + event.key
                + self.value[self._cursor_position :]
            )
            self._cursor_position += len(event.key)

        self.refresh()
