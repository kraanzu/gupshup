import logging
import os
from queue import Queue
from textual.app import App
from textual import events, message, message_pump
from sys import argv
from collections import defaultdict
from textual.layouts.dock import DockLayout

from textual.reactive import Reactive
from textual.widgets import ScrollView, TreeClick, Static
from .widgets import (
    Footbar,
    Headbar,
    ChatScreen,
    TextInput,
    HouseTree,
    MemberList,
    Banner,
)

from src import Client
from src.utils import Message

logging.basicConfig(filename="tui.log", encoding="utf-8", level=logging.DEBUG)

percent = lambda percent, total: int(percent * total / 100)


class Tui(App):
    async def on_load(self, _: events.Load) -> None:
        self.user = argv[1]
        self.queue = Queue()
        self.client = Client(self.user, self.queue)
        self.client.start_connection()
        self.current_house = "HOME"
        self.current_room = "general"
        self.current_screen = f"{self.current_house}/{self.current_room}"

        self.member_lists: dict[str, MemberList] = defaultdict(MemberList)

        self.set_interval(0.2, self.server_listen)

        await self.bind("ctrl+b", "view.toggle('sidebar')", "toggle sidebar")
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind(
            "escape", "reset_focus", "resets focus to the header", show=False
        )

    async def on_key(self, event: events.Key):
        if event.key == "enter":
            await self.action_send_message()

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

    async def perform_push_text(self, message: Message):
        screen = f"{message.house}/{message.room}"
        self.chat_screen[screen].push_text(message)
        if self.current_screen == screen:
            await self.refresh_screen()

    async def perform_add_house(self, message: Message):
        await self.house_tree.add_house(message.text)

    async def perform_add_room(self, message: Message):
        await self.house_tree.add_room(message.house, message.text)

    async def perform_del_room(self, message: Message):
        self.house_tree.del_room(message.house, message.room)

    async def perform_del_house(self, message: Message):
        self.house_tree.del_house(message.house)
        await self.update_chat_screen("HOME", "general")

    async def perform_add_rank(self, message: Message):
        await self.member_lists[message.house].add_rank(message.text)

    async def perform_del_rank(self, message: Message):
        await self.member_lists[message.house].del_rank(message.text)

    async def perform_add_user_rank(self, message: Message):
        await self.member_lists[message.house].add_user_to_rank(
            message.data["rank"], message.data["user"]
        )

    async def perform_del_user_rank(self, message: Message):
        await self.member_lists[message.house].del_from_rank(
            message.data["rank"], message.data["user"]
        )

    async def execute_message(self, message: Message) -> None:
        cmd = f"self.perform_{message.action}(message)"
        await eval(cmd)

    async def server_listen(self) -> None:
        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        y = os.get_terminal_size()[1]
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.input_box = TextInput(placeholder="Speak your mind here...")

        self.banner = Banner()
        self.chat_screen = defaultdict(ChatScreen)

        self.house_tree = HouseTree()
        await self.house_tree.add_house("HOME")
        await self.house_tree.root.expand()

        self.rseperator = self.lseperator = "\n" * percent(12, y) + "┃\n" * percent(
            75, y
        )

        self.set_interval(0.8, self.server_listen)
        await self.refresh_screen()

    async def refresh_screen(self):
        # clears all the widgets from the screen..and re render them all
        # Why? you ask? this was the only way at the time of this writing

        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

        x, y = os.get_terminal_size()
        await self.view.dock(self.headbar, name="headbar")
        await self.member_lists[self.current_house].root.expand()

        # RIGHT WIDGETS
        if self.current_house != "HOME":
            await self.view.dock(
                (self.member_lists[self.current_house]),
                edge="right",
                size=int(0.15 * x),
                name="member_list",
            )
            await self.view.dock(
                Static(self.rseperator), edge="right", size=1, name="rs"
            )

        # LEFT WIDGETS
        await self.view.dock(
            self.house_tree,
            edge="left",
            size=percent(15, x),
            name="house_tree",
        )
        await self.view.dock(Static(self.lseperator), edge="left", size=1, name="ls")

        # MIDDLE WIDGETS
        await self.view.dock(
            self.banner,
            size=percent(10, y),
            name="current_screen_bar",
        )
        await self.view.dock(
            ScrollView(self.chat_screen[self.current_screen], gutter=(0, 1)),
            size=percent(75, y),
            name="chat_screen",
        )
        await self.view.dock(self.input_box, size=percent(10, y), name="input_box")

    async def update_chat_screen(self, house: str, room: str):
        if self.current_house == house and self.current_room == room:
            return

        self.current_house = house
        self.current_room = room
        self.current_screen = f"{self.current_house}/{self.current_room}"

        self.banner.set_text(self.current_screen)
        self.house_tree.select(self.current_house, self.current_room)

        await self.refresh_screen()

    async def handle_tree_click(self, click: TreeClick):
        node = click.node
        match node.data.type:
            case "room":
                if node.parent:
                    house = str(node.parent.label)
                    room = str(node.label)
                    await self.update_chat_screen(
                        house,
                        room,
                    )
            case "house":
                await node.toggle()

            # FOR MEMEBER LISTS
            case "rank":
                await node.toggle()

            case "member":
                await self.update_chat_screen("HOME", "general")

    async def action_reset_focus(self):
        await self.headbar.focus()
