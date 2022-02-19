import os
from queue import Queue
from textual import events
from sys import argv
from collections import defaultdict

from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widgets import ScrollView, TreeClick, Static
from .widgets import (
    Headbar,
    ChatScreen,
    TextInput,
    HouseTree,
    MemberList,
    Banner,
)

from ..src import Client
from ..src.utils import Message, HouseData, House

percent = lambda percent, total: int(percent * total / 100)


class Tui(App):
    """
    The UI Class for Gupshup
    """

    async def on_load(self, _: events.Load) -> None:

        # INITS

        # client related
        self.queue = Queue()
        self.user = argv[1]
        self.client = Client(self.user, self.queue)

        # sets up default screen
        self.current_house = "HOME"
        self.current_room = "general"
        self.current_screen = f"{self.current_house}/{self.current_room}"

        self.member_lists: dict[str, MemberList] = defaultdict(MemberList)

        # some keybindings
        await self.bind("ctrl+b", "view.toggle('house_tree')", "toggle house tree")
        await self.bind("ctrl+q", "quit", "Quit")
        await self.bind(
            "escape", "reset_focus", "resets focus to the header", show=False
        )

    async def on_key(self, event: events.Key):
        if event.key == "enter":
            await self.action_send_message()
        else:
            if self.input_box.has_focus:
                await self.input_box.keypress(event.key)
                event.stop()

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
                house.name, room, "icon", house.room_icons.get(room, "")
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
        self.chat_screen[screen].push_text(message)

        if not local:  # check if local/offline data is not being pushed
            if self.current_screen == screen:
                await self.chat_scroll.update(
                    self.chat_screen[screen].chats, home=False
                )
                self.chat_scroll.animate(
                    "y",
                    self.chat_scroll.max_scroll_y + self.chat_scroll.y,
                    easing="none",
                )
            else:
                if not self.house_tree.is_room_silent(message.house, message.room):
                    self.console.bell()
                self.house_tree.increase_pending(message.house, message.room)

    async def perform_add_room(self, message: Message) -> None:
        await self.house_tree.add_room(message.house, message.text)

    async def perform_del_chat(self, message: Message) -> None:
        self.house_tree.del_room(message.house, message.room)
        self.chat_screen[f"{message.house}/{message.room}"].chats = ""
        await self.update_chat_screen(message.house, "general")

    async def perform_clear_chat(self, message: Message) -> None:
        screen = f"{message.house}/{message.room}"
        self.chat_screen[screen].chats = ""
        if screen == self.current_screen:
            await self.chat_scroll.update("")

    async def perform_del_room(self, message: Message) -> None:
        self.house_tree.del_room(message.house, message.room)
        if self.current_house == message.house and self.current_room == message.room:
            await self.update_chat_screen(message.house, "general")

    async def perform_del_house(self, message: Message) -> None:
        self.house_tree.del_house(message.house)
        await self.update_chat_screen("HOME", "general")

    async def perform_add_rank(self, message: Message) -> None:
        await self.member_lists[message.house].add_rank(message.text)

    async def perform_del_rank(self, message: Message) -> None:
        await self.member_lists[message.house].del_rank(message.text)

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
            message.data["rank"], "color", message.data["color"]
        )

    async def perform_change_rank_name(self, message: Message) -> None:
        await self.member_lists[message.house].change_rank_name(
            message.data["rank"], message.data["name"]
        )

    async def perform_change_rank_icon(self, message: Message) -> None:
        await self.member_lists[message.house].change_rank_data(
            message.data["rank"], "icon", message.data["icon"]
        )

    async def perform_change_room_name(self, message: Message) -> None:
        self.house_tree.change_room_name(message.house, message.room, message.text)
        self.chat_screen[f"{message.house}/{message.text}"] = self.chat_screen[
            f"{message.house}/{message.room}"
        ]
        del self.chat_screen[f"{message.house}/{message.room}"]
        await self.update_chat_screen(message.house, message.text)

    async def perform_change_room_icon(self, message: Message) -> None:
        self.house_tree.change_room_data(
            message.house, message.room, "icon", message.text
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
        if self.queue.qsize():
            message = self.queue.get()
            await self.execute_message(message)

    async def on_mount(self, _: events.Mount) -> None:
        y = os.get_terminal_size()[1]

        self.title = "Welcome to Gupshup"
        self.headbar = Headbar()
        self.input_box = TextInput(placeholder="Say something here...")

        self.banner = Banner()
        self.chat_screen = defaultdict(ChatScreen)
        self.chat_scroll = ScrollView(gutter=(0, 1))

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
        self.set_interval(0.2, self.server_listen)

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

        await self.chat_scroll.update(
            self.chat_screen[self.current_screen].chats,
            home=False
            # (home = False) so that it doesn't scroll back each and every time when updated
        )

        self.member_list_scroll = ScrollView(self.member_lists[self.current_house])

        self.chat_scroll.animate(
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
            await self.view.dock(
                self.member_lists[self.current_house],
                edge="right",
                size=int(0.15 * x),
                name="member_list",
            )
            await self.view.dock(
                Static(self.rseperator), edge="right", size=1, name="rs"
            )

        # LEFT WIDGETS
        await self.view.dock(
            self.house_tree_scroll,
            edge="left",
            size=percent(20, x),
            name="house_tree",
        )
        await self.view.dock(Static(self.lseperator), edge="left", size=1, name="ls")

        # MIDDLE WIDGETS
        await self.view.dock(
            self.banner,
            size=percent(10, y),
            name="banner",
        )
        await self.view.dock(
            self.chat_scroll,
            size=percent(75, y),
            name="chat_screen",
        )

        await self.view.dock(self.input_box, size=percent(10, y), name="input_box")
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
