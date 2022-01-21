import logging
import asyncio
from queue import Queue
from textual.app import App
from textual import events

from ui.utils import Footbar, Headbar, ChatScreen, TextInput
from tests import client
from queue import Queue


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
        self.headbar = Headbar()
        self.chatscreen = ChatScreen(queue=self.queue)
        self.ibox = TextInput()
        self.footbar = Footbar()

        await self.view.dock(self.headbar)
        await self.view.dock(self.chatscreen, size=25)
        await self.view.dock(self.footbar, self.ibox, edge="bottom")

    async def action_reset_focus(self):
        await self.headbar.focus()
