import logging
import os
from queue import Queue
from textual.app import App
from textual import events

from textual.widgets import ScrollView
from .widgets import Footbar, Headbar, ChatScreen, TextInput, HouseTree, MemberList

from src import Client

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)

class Tui(App):
    async def on_load(self, _: events.Load) -> None:
        user = "test"
        self.queue = Queue()
        self.client = Client(user, self.queue)
        self.client.start_connection()
        self.current_house = user
        self.current_room = "general"

        self.set_interval(0.2, self.server_listen)

        await self.bind("b", "view.toggle('sidebar')", "toggle sidebar")
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind(
            "escape", "reset_focus", "resets focus to the header", show=False
        )
        await self.bind("ctrl+s", "send_message")

    async def action_send_message(self):
        value = self.input_box.value.strip().strip('\n')
        if not value:
            return

        self.chat_screen.push_text(value)
        self.client.send(text=value, house=self.current_house, room=self.current_room)
        self.input_box.value = ""
        self.input_box.refresh()

    def execute_data(self) -> None:
        pass

    async def server_listen(self) -> None:
        if self.queue.qsize():
            message = self.queue.get()
            self.chat_screen.push_text(message.text)

    async def on_mount(self, _: events.Mount) -> None:
        x, y = os.get_terminal_size()
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.input_box = TextInput()
        self.chat_screen = ChatScreen(queue=self.queue)
        self.house_tree = HouseTree("House Tree")
        self.member_list = MemberList("Member List")
        self.set_interval(0.2, self.server_listen)

        await self.view.dock(self.headbar, name="headbar")
        await self.view.dock(
            ScrollView(self.member_list),
            edge="right",
            size=int(0.15 * x),
            name="member_list",
        )
        await self.view.dock(
            self.house_tree, edge="left", size=int(0.15 * x), name="house_tree"
        )
        await self.view.dock(self.chat_screen, size=int(0.85 * y), name="chat_screen")
        await self.view.dock(self.input_box, edge="bottom", name="input_box")

    async def action_reset_focus(self):
        await self.headbar.focus()
