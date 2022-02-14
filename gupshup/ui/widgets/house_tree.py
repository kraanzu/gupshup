from rich.text import Text
from rich.console import RenderableType
from textual.widgets import TreeNode

from .custom_tree import CustomTree
from ...src.utils import CustomNode


class HouseTree(CustomTree):
    def __init__(self) -> None:
        name = Text("House Tree", style="bold red")
        self.selected = ["HOME", "general"]
        super().__init__(name, CustomNode(type="house_root", icon=""))

    def render_node(self, node: TreeNode) -> RenderableType:
        return self.render_tree_label(
            node,
            node.id == self.hover_node,
        )

    def render_tree_label(
        self,
        node: TreeNode,
        is_hover: bool,
    ) -> RenderableType:
        """
        Custom highlight for different parts of node
        """

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = Text(node.label) if isinstance(node.label, str) else node.label
        label.stylize(node.data.color)

        if node.data.type == "house_root":
            color = "bold red"
        elif node.data.type == "house":
            color = "green " if str(node.label) == self.selected[0] else "blue "
        else:
            color = (
                "green"
                if str(node.label) == self.selected[1]
                # SAFETY: The only else option is `room` and a room will always have a parent
                and str(node.parent.label) == self.selected[0]
                else "white"
            )
        label.stylize(color)

        if is_hover:
            label.stylize("bold red" if node.data.type == "house_root" else "magenta")

        icon_label = (
            Text(
                f"{'ﱝ ' if node.data.silent else ' '}" + f"{node.data.icon} ",
                no_wrap=True,
                overflow="ellipsis",
            )
            + label
        )

        if node.data.pending != "0":
            icon_label += f"({node.data.pending})"

        icon_label.apply_meta(meta)
        return icon_label

    async def expand_home(self) -> None:
        """
        Expands `HOME` group
        """

        node = self.root.children[self.get_node_index(self.root, "HOME")]
        await node.expand()

    def select(self, house: str, room: str) -> None:
        """
        Selects the current screen for a color hint
        """

        self.selected = [house, room]

    def is_room_silent(self, house: str, room: str) -> bool:
        house_node = self.root.children[self.get_node_index(self.root, house)]
        room_node = house_node.children[self.get_node_index(house_node, room)]
        return room_node.data.silent

    async def add_house(self, name: str) -> None:
        await super().add_under_root(name, CustomNode(type="house", icon="ﳐ"))
        await self.add_room(name, "general")
        self.refresh(layout=True)

    async def add_room(self, house: str, name: str) -> None:
        """
        Adds a room if not already present
        """
        # Q: why the checking `if already present` ? for DIRECT messages

        await self.add_under_child(house, name, CustomNode(type="room", icon="ﴘ"))
        self.refresh()

    def del_house(self, name: str) -> None:
        super().del_under_root(name)
        self.refresh()

    def del_room(self, house: str, room: str) -> None:
        super().del_under_child(house, room)
        self.refresh()

    def toggle_silent(self, house: str, room: str) -> None:
        """
        Toggle the current silent option for a room
        """

        house_node = self.root.children[self.get_node_index(self.root, house)]
        room_node = house_node.children[self.get_node_index(house_node, room)]
        room_node.data.silent = not room_node.data.silent
        self.refresh()

    def change_house_name(self, house: str, name: str) -> None:
        super().change_name_parent(house, name)

    def change_house_data(self, house: str, param: str, value: str) -> None:
        """
        Changes house data such as icon or color
        """

        super().change_data_parent(house, param, value)

    def change_room_name(self, house: str, room: str, name: str) -> None:
        super().change_name_child(house, room, name)

    def change_room_data(self, house: str, room: str, param: str, value: str) -> None:
        """
        Changes room data such as icon or name
        """
        super().change_data_child(house, room, param, value)

    def increase_pending(self, house: str, room: str) -> None:
        """
        Increase the pending messages of the chat or room by 1
        """

        current_pending = int(super().get_data_child(house, room, "pending"))
        super().change_data_child(house, room, "pending", str(current_pending + 1))
        self.refresh()
