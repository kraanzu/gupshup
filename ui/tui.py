import logging
import os
from queue import Queue
from textual.app import App
from textual import events

from textual.widgets import TreeClick
from .widgets import Footbar, Headbar, ChatScreen, TextInput, HouseTree
from tests import client


logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class Tui(App):
    async def on_load(self, _: events.Load) -> None:
        self.queue = Queue()
        self.client = client(self.queue)
        self.client.start_connection()

        await self.bind("b", "view.toggle('sidebar')", "toggle sidebar")
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind("ctrl-n", "", "next room")
        await self.bind("ctrl-p", "", "previous room")
        await self.bind(
            "escape", "reset_focus", "resets focus to the header", show=False
        )
        await self.bind("ctrl+s", "send_message")

    async def action_send_message(self):
        value = self.ibox.value
        self.chatscreen.push_text(value)
        self.client.send(value)
        self.ibox.value = ""
        self.ibox.refresh()

    async def on_mount(self, _: events.Mount) -> None:
        x, y = os.get_terminal_size()
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.ibox = TextInput()
        self.chatscreen = ChatScreen(queue=self.queue)
        self.house_tree = HouseTree("House Tree")

        await self.view.dock(self.headbar)
        await self.view.dock(
            self.house_tree, edge="left", size=int(0.2 * x), name="sidebar"
        )
        await self.view.dock(self.chatscreen, size=int(0.85 * y))
        await self.view.dock(self.ibox, edge="bottom")

    async def action_reset_focus(self):
        await self.headbar.focus()
