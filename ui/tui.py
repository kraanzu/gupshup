import logging
import os
from queue import Queue
from textual.app import App
from textual import events
from sys import argv
from collections import defaultdict

from textual.widgets import ScrollView, TreeClick
from .widgets import Footbar, Headbar, ChatScreen, TextInput, HouseTree, MemberList

from src import Client
from src.utils import Message

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)


class Tui(App):
    async def on_load(self, _: events.Load) -> None:
        self.user = argv[1]
        self.queue = Queue()
        self.client = Client(self.user, self.queue)
        self.client.start_connection()
        self.current_house = self.user
        self.current_room = "general"
        self.current_screen = f"{self.current_house}/{self.current_room}"
        self.member_lists: dict[str, MemberList] = defaultdict(MemberList)

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
        screen = f"{message.house}/{message.room}"
        match message.action:
            case "push_text":
                self.chat_screen.push_text(screen, message.text)
            case "add_room":
                await self.house_tree.add_room(message.house, message.text)

    async def server_listen(self) -> None:
        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        x, y = os.get_terminal_size()
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.input_box = TextInput()
        self.chat_screen = ChatScreen()
        self.chat_screen.set_current_screen(self.current_screen)
        self.house_tree = HouseTree()
        await self.house_tree.add_house(self.user)
        await self.house_tree.add_room(self.user, "general")
        await self.house_tree.root.expand()
        self.member_list = MemberList()
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

    async def update_chat_screen(self, house: str, room: str):
        self.current_house = house
        self.current_room = room
        self.current_screen = f"{self.current_house}/{self.current_room}"
        self.chat_screen.set_current_screen(self.current_screen)
        self.chat_screen.refresh()

    async def handle_tree_click(self, click: TreeClick):
        node = click.node
        match node.data:
            # FOR HOUSE TREE
            case "room":
                # SAFETY: a node with label `room` will always have a parent
                if node.parent:
                    house = str(node.parent.label)
                    room = str(node.label)
                    await self.update_chat_screen(
                        house,
                        room,
                    )
            case "house":
                if self.current_house == str(node.label):
                    await node.toggle()
                else:
                    await self.update_chat_screen(str(node.label), "general")

            # FOR MEMEBER LISTS
            case "rank":
                await node.toggle()

            case "member":
                await self.update_chat_screen(self.user, str(node.label))

            case _:
                pass

    async def action_reset_focus(self):
        await self.headbar.focus()
