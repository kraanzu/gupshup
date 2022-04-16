import os
import asyncio
from collections import defaultdict
from queue import Queue
from typing import Type

from rich.console import Console
from rich.align import Align
from rich.text import Text

from textual import events
from textual.driver import Driver
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widgets import ScrollView, TreeClick, Static
from textual_extras.widgets import TextInput

from .widgets import (
    Headbar,
    ChatScreen,
    HouseTree,
    MemberList,
    Banner,
)
from ..src import Client
from ..src.utils import Message, HouseData, HELP_TEXT, notify


def percent(percent, total):
    return int(percent * total / 100)


class Tui(App):
    """
    The UI Class for Gupshup
    """

    def __init__(
        self,
        user: str,
        quiet: bool = False,
        screen: bool = True,
        driver_class: Type[Driver] | None = None,
        log: str = "",
        log_verbosity: int = 1,
        title: str = "Textual Application",
    ):
        super().__init__(
            screen=screen,
            driver_class=driver_class,
            log=log,
            log_verbosity=log_verbosity,
            title=title,
        )
        self.user = user
        self.quiet = quiet

    @classmethod
    def run(
        cls,
        user,
        quiet,
        console: Console = None,
        screen: bool = True,
        driver: Type[Driver] = None,
        **kwargs,
    ):
        """Run the app.

        Args:
            console (Console, optional): Console object. Defaults to None.
            screen (bool, optional): Enable application mode. Defaults to True.
            driver (Type[Driver], optional): Driver class or None for default. Defaults to None.
        """

        async def run_app() -> None:
            app = cls(
                user=user, quiet=quiet, screen=screen, driver_class=driver, **kwargs
            )
            await app.process_messages()

        asyncio.run(run_app())

    async def on_load(self, _: events.Load) -> None:

        # client related
        self.queue = Queue()
        self.client = Client(self.user, self.queue)

        # sets up default screen
        self.current_house = "HOME"
        self.current_room = "general"
        self.current_screen = f"{self.current_house}/{self.current_room}"
        self.help_menu_loaded = False

        self.member_lists: dict[str, MemberList] = defaultdict(MemberList)
        self.member_scrolls: dict[str, ScrollView] = defaultdict(ScrollView)

        # some keybindings
        await self.bind(
            "ctrl+b",
            "view.toggle('house_tree')",
            "toggle house tree",
        )
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind(
            "escape",
            "reset_focus",
            "resets focus to the header",
            show=False,
        )

        self.set_interval(
            0.1, self.refresh
        )  # deal with rendering issues when toggled house tree

    def set_client(self, name: str) -> None:
        self.user = name

    async def load_help_menu(self):
        banner = """
        ┬ ┬┌─┐┬  ┌─┐  ┌┬┐┌─┐┌┐┌┬ ┬
        ├─┤├┤ │  ├─┘  │││├┤ ││││ │
        ┴ ┴└─┘┴─┘┴    ┴ ┴└─┘┘└┘└─┘
        """
        await self._clear_screen()
        await self.view.dock(
            Static(Align.center(Text(banner, style="magenta"), vertical="middle")),
            size=percent(20, os.get_terminal_size()[1]),
        )
        await self.view.dock(
            Static(
                Align.center(
                    Text("-- Press ctrl+p to exit --", style="bold magenta"),
                    vertical="middle",
                )
            ),
            edge="bottom",
            size=percent(10, os.get_terminal_size()[1]),
        )
        await self.view.dock(ScrollView(Align.center(HELP_TEXT)))

    async def on_key(self, event: events.Key):
        if event.key == "ctrl+p":
            if self.help_menu_loaded:
                await self.refresh_screen()
            else:
                await self.load_help_menu()

            self.help_menu_loaded = not self.help_menu_loaded

        elif event.key == "enter":
            await self.action_send_message()

    async def action_send_message(self):
        """
        Empties the input box and sends the message to the server
        """

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
        self.input_box.clear()

    # +-------------------------------+
    # | Methods to manage message     |
    # | when recieved from the server |
    # +-------------------------------+

    # SYNTAX : perform_<action>(message: Message) -> None
    async def perform_add_house(
        self,
        message: Message,
    ) -> None:
        """
        Attaches a house to the tree
        """

        house: HouseData = message.data["house"]
        await self.house_tree.add_house(house.name)

        for room in house.rooms:
            await self.house_tree.add_room(house.name, room)
            self.house_tree.change_data_child(
                house.name,
                room,
                "icon",
                house.room_icons.get(room, ""),
            )

        for name, rank in house.ranks.items():
            await self.member_lists[house.name].add_rank(name)
            self.member_lists[house.name].change_data_parent(name, "color", rank.color)
            self.member_lists[house.name].change_data_parent(name, "icon", rank.icon)

        for name, rank in house.member_rank.items():
            await self.member_lists[house.name].add_user_to_rank(rank, name)

    async def perform_connection_disable(self, *_) -> None:
        self.headbar.status = "ﮡ Can't connect"

    async def perform_connection_enable(self, *_) -> None:
        self.headbar.status = " Online"

    async def perform_push_text(self, message: Message, local=False) -> None:
        """
        Performs adding all the text messages to their respective locations
        """
        screen = f"{message.house}/{message.room}"
        await self.chat_screen[screen].push_text(message)

        if not local:  # check if local/offline data is not being pushed
            if self.current_screen == screen:
                self.chat_screen[self.current_screen].refresh(layout=True)
            else:
                if (
                    not self.house_tree.is_room_silent(message.house, message.room)
                    and not self.quiet
                ):
                    notify()

                self.house_tree.increase_pending(message.house, message.room)

    async def perform_add_room(self, message: Message) -> None:
        await self.house_tree.add_room(message.house, message.data["room"])

    async def perform_clear_chat(self, message: Message) -> None:
        screen = f"{message.house}/{message.room}"
        await self.chat_screen[screen].clear_chat()
        if screen == self.current_screen:
            self.chat_screen[screen].refresh()

    async def perform_archive(self, message: Message) -> None:
        screen = f"{message.house}/{message.room}"

        self.house_tree.del_room(message.house, message.room)
        if self.current_screen == screen:
            await self.update_chat_screen(message.house, "general")

    async def perform_del_room(self, message: Message) -> None:
        screen = f"{message.house}/{message.room}"
        await self.chat_screen[screen].clear_chat()
        await self.perform_archive(message)

    async def perform_del_house(self, message: Message) -> None:
        self.house_tree.del_house(message.house)
        await self.update_chat_screen("HOME", "general")

    async def perform_add_rank(self, message: Message) -> None:
        await self.member_lists[message.house].add_rank(message.data["rank"])

    async def perform_del_rank(self, message: Message) -> None:
        await self.member_lists[message.house].del_rank(message.data["rank"])

    async def perform_add_user_rank(self, message: Message) -> None:
        await self.member_lists[message.house].add_user_to_rank(
            message.data["rank"], message.data["user"]
        )

    async def perform_del_user_rank(self, message: Message) -> None:
        await self.member_lists[message.house].del_from_rank(
            message.data["rank"], message.data["user"]
        )

    async def perform_change_rank_color(self, message: Message) -> None:
        await self.member_lists[message.house].change_rank_data(
            message.data["rank"],
            "color",
            message.data["color"],
        )

    async def perform_change_rank_name(self, message: Message) -> None:
        await self.member_lists[message.house].change_rank_name(
            message.data["rank"], message.data["name"]
        )

    async def perform_change_rank_icon(self, message: Message) -> None:
        await self.member_lists[message.house].change_rank_data(
            message.data["rank"],
            "icon",
            message.data["icon"],
        )

    async def perform_change_room_name(self, message: Message) -> None:
        name = message.data["name"]
        self.house_tree.change_room_name(message.house, message.room, name)
        self.chat_screen[f"{message.house}/{name}"] = self.chat_screen[
            f"{message.house}/{message.room}"
        ]
        del self.chat_screen[f"{message.house}/{message.room}"]
        await self.update_chat_screen(message.house, name)

    async def perform_change_room_icon(self, message: Message) -> None:
        self.house_tree.change_room_data(
            message.house,
            message.room,
            "icon",
            message.data["icon"],
        )

    async def perform_toggle_silent(self, message: Message) -> None:
        self.house_tree.toggle_silent(message.house, message.room)

    async def execute_message(self, message: Message) -> None:
        """
        Executes the messages recieved from the server
        """

        cmd = f"self.perform_{message.action}(message)"
        await eval(cmd)

    async def server_listen(self) -> None:
        """
        Method to continously listen for new messages from the server
        """

        # Is being called every 0.1 seconds to update
        # Proposal for a `call_threaded` function has not been merged yet..
        # see: https://github.com/Textualize/textual/issues/85

        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        y = os.get_terminal_size()[1]

        self.title = "Welcome to Gupshup"
        self.headbar = Headbar()
        self.input_box = TextInput(
            placeholder=Text("Say something here...", style="dim white")
        )

        self.banner = Banner()
        self.chat_screen = defaultdict(ChatScreen)
        self.chat_scroll = defaultdict(ScrollView)

        self.house_tree = HouseTree()
        await self.house_tree.add_house("HOME")
        await self.house_tree.root.expand()

        self.rseperator = self.lseperator = "\n" * percent(12, y) + "┃\n" * percent(
            75, y
        )

        self.house_tree_scroll = ScrollView(self.house_tree)
        self.member_list_scroll = ScrollView(self.member_lists[self.current_house])

        await self.populate_local_data()
        await self.refresh_screen()

    async def populate_local_data(self) -> None:
        """
        Populates the app with offline data stored in the system
        """

        for message in self.client.chats:
            if message.action == "push_text":
                await self.perform_push_text(message, local=True)
            else:
                await eval(f"self.perform_{message.action}(message)")

        self.client.start_connection()
        self.set_interval(0.1, self.server_listen)

    async def on_resize(self, _: events.Resize) -> None:
        await self.refresh_screen()

    async def action_quit(self) -> None:
        """
        Clean quit saving the data
        """
        self.client.save_chats()
        await super().action_quit()

    async def _clear_screen(self) -> None:
        # clears all the widgets from the screen..and re render them all
        # Why? you ask? this was the only way at the time of this writing

        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

    async def refresh_screen(self) -> None:
        """
        Refresh the screen by repainting all the widgets
        """

        await self._clear_screen()
        x, y = os.get_terminal_size()

        if self.current_screen not in self.chat_scroll:
            self.chat_scroll[self.current_screen] = ScrollView(
                self.chat_screen[self.current_screen],
                gutter=(0, 1),
            )

        if self.current_house not in self.member_scrolls:
            self.member_scrolls[self.current_house] = ScrollView(
                self.member_lists[self.current_house]
            )

        self.chat_scroll[self.current_screen].animate(
            "y",
            10**5,
            # A large enough value to make sure it really scrolls down to the end
            # ..will have to probably change this
            easing="none",
            speed=1000,
        )

        await self.view.dock(self.headbar, name="headbar")
        await self.member_lists[self.current_house].root.expand()

        # RIGHT WIDGETS
        if self.current_house != "HOME":
            # There is *NO* member list for `HOME`
            await self.view.dock(
                self.member_scrolls[self.current_house],
                edge="right",
                size=int(0.15 * x),
                name="member_list",
            )
            await self.view.dock(
                Static(self.rseperator),
                edge="right",
                size=1,
                name="rs",
            )

        # LEFT WIDGETS
        await self.view.dock(
            self.house_tree_scroll,
            edge="left",
            size=percent(20, x),
            name="house_tree",
        )
        await self.view.dock(
            Static(self.lseperator),
            edge="left",
            size=1,
            name="ls",
        )

        # MIDDLE WIDGETS
        await self.view.dock(
            self.banner,
            size=percent(10, y),
            name="banner",
        )
        await self.view.dock(
            self.chat_scroll[self.current_screen],
            size=percent(75, y),
            name="chat_screen",
        )

        await self.view.dock(
            self.input_box,
            size=percent(10, y),
            name="input_box",
        )
        self.refresh(layout=True)  # A little bit too cautious

    async def update_chat_screen(self, house: str, room: str):
        """
        Update the screen when the chat is changed
        """
        # TODO: Make this reactive

        if self.current_house == house and self.current_room == room:
            return

        self.current_house = house
        self.current_room = room
        self.current_screen = f"{self.current_house}/{self.current_room}"

        self.house_tree.change_room_data(house, room, "pending", "0")
        self.banner.set_text(self.current_screen)
        self.house_tree.select(self.current_house, self.current_room)

        await self.refresh_screen()

    async def handle_tree_click(self, click: TreeClick) -> None:
        """
        Handles various clicks
        """
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
            case "house" | "rank":
                await node.toggle()
                self.refresh(layout=True)

            case "member":
                name = str(node.label)
                if name == self.user:
                    return

                await self.house_tree.add_room("HOME", name)
                await self.house_tree.expand_home()
                await self.update_chat_screen("HOME", name)

    async def action_reset_focus(self):
        await self.headbar.focus()
