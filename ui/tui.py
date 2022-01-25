import logging
import os
from queue import Queue
from textual.app import App
from textual import events

from textual.widgets import ScrollView
from .widgets import Footbar, Headbar, ChatScreen, TextInput, HouseTree, MemberList

from src import Client
from src.utils import Message

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class Tui(App):
    async def on_load(self, _: events.Load) -> None:
        self.user = "test"
        self.queue = Queue()
        self.client = Client(self.user, self.queue)
        self.client.start_connection()
        self.current_house = self.user
        self.current_room = "general"

        self.set_interval(0.2, self.server_listen)

        await self.bind("b", "view.toggle('sidebar')", "toggle sidebar")
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind(
            "escape", "reset_focus", "resets focus to the header", show=False
        )
        await self.bind("ctrl+s", "send_message")

    async def action_send_message(self):
        value = self.input_box.value.strip().strip("\n")
        if not value:
            return

        self.chat_screen.push_text(value)
        self.client.send(
            Message(
                sender=self.user,
                house=self.current_house,
                room=self.current_room,
                text=value,
            )
        )
        self.input_box.value = ""
        self.input_box.refresh()

    async def execute_message(self, message: Message) -> None:
        match message.action:
            case "push_text":
                self.chat_screen.push_text(message.text)
            case "add_room":
                await self.house_tree.add_house(message.text)

    async def server_listen(self) -> None:
        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        x, y = os.get_terminal_size()
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.input_box = TextInput()
        self.chat_screen = ChatScreen(queue=self.queue)
        self.house_tree = HouseTree("House Tree")
        await self.house_tree.root.expand()
        self.member_list = MemberList("Member List")
        await self.member_list.root.expand()
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
