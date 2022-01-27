import logging
import os
from queue import Queue
from textual.app import App
from textual import events
from sys import argv
from collections import defaultdict

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
from rich.panel import Panel

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
        await self.bind("ctrl+s", "send_message")

    async def hide_right_side(self):
        self.view.named_widgets["rs"].visible = False
        self.view.named_widgets["member_list"].visible = False

    async def unhide_right_side(self):
        self.view.named_widgets["rs"].visible = True
        self.view.named_widgets["member_list"].visible = True

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
            case "add_house":
                await self.house_tree.add_house(message.text)
            case "add_room":
                await self.house_tree.add_room(message.house, message.text)
            case _:
                self.chat_screen.push_text(screen, message.text)

        await self.chat_scroll.update(self.chat_screen.render())

    async def server_listen(self) -> None:
        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        x, y = os.get_terminal_size()
        self.headbar = Headbar()
        self.footbar = Footbar()
        self.input_box = TextInput(placeholder="Speak your mind here...")

        self.banner = Banner()
        self.chat_screen = ChatScreen()
        self.chat_scroll = ScrollView(gutter=(0, 1))
        self.chat_screen.set_current_screen(self.current_screen)

        self.house_tree = HouseTree()
        await self.house_tree.add_house("HOME")
        await self.house_tree.root.expand()

        self.member_list = self.member_lists[self.current_screen]
        await self.member_list.root.expand()

        self.rseperator = self.lseperator = "\n" * percent(12, y) + "┃\n" * percent(
            75, y
        )

        self.set_interval(0.2, self.server_listen)

        await self.view.dock(self.headbar, name="headbar")

        # RIGHT WIDGETS
        await self.view.dock(
            ScrollView(self.member_list),
            edge="right",
            size=int(0.15 * x),
            name="member_list",
        )
        await self.view.dock(Static(self.rseperator), edge="right", size=1, name="rs")

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
            (self.banner),
            size=percent(10, y),
            name="current_screen_bar",
        )
        await self.hide_right_side()
        await self.view.dock(self.chat_scroll, size=percent(75, y), name="chat_screen")
        await self.view.dock(self.input_box, size=percent(10, y), name="input_box")
        self.view.border = "blue"

    async def update_chat_screen(self, house: str, room: str):
        self.current_house = house
        self.current_room = room
        self.current_screen = f"{self.current_house}/{self.current_room}"
        self.chat_screen.set_current_screen(self.current_screen)
        self.banner.set_text(self.current_screen)
        self.house_tree.select(self.current_house, self.current_room)

        await (
            self.hide_right_side()
            if self.current_house == "HOME"
            else self.unhide_right_side()
        )

        self.member_list = self.member_lists[self.current_house]
        await self.chat_scroll.update(self.chat_screen.render())

        self.chat_scroll.refresh()
        self.view.refresh()

    async def handle_tree_click(self, click: TreeClick):
        node = click.node
        match node.data.type:
            # FOR HOUSE TREE
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
                await self.update_chat_screen(self.user, str(node.label))

    async def action_reset_focus(self):
        await self.headbar.focus()
