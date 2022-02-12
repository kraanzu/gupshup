from rich.text import Text
from rich.console import RenderableType
from textual.widgets import TreeNode

from .custom_tree import CustomTree
from ...src.utils import CustomNode


class HouseTree(CustomTree):
    def __init__(self) -> None:
        name = Text("House Tree", style="bold red")
        self.selected = ["", ""]
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
    ):

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

        icon = node.data.icon
        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label

        if node.data.silent:
            icon_label += Text(" ﱝ", no_wrap=True, overflow="ellipsis")

        if node.data.pending != "0":
            icon_label += Text(
                f" ({node.data.pending})", no_wrap=True, overflow="ellipsis"
            )

        icon_label.apply_meta(meta)

        return icon_label

    async def expand_home(self):
        node = self.root.children[self.get_node_index(self.root, "HOME")]
        await node.expand()

    def select(self, house: str, room: str):
        self.selected = [house, room]

    def is_room_silent(self, house: str, room: str):
        house_node = self.root.children[self.get_node_index(self.root, house)]
        room_node = house_node.children[self.get_node_index(house_node, room)]
        return room_node.data.silent

    async def add_house(self, name: str) -> None:
        await super().add_under_root(name, CustomNode(type="house", icon="ﳐ"))
        await self.add_room(name, "general")
        self.refresh()

    async def add_room(self, house: str, name: str) -> None:
        await self.add_under_child(house, name, CustomNode(type="room", icon="ﴘ"))
        self.refresh()

    def del_house(self, name: str):
        super().del_under_root(name)
        self.refresh()

    def del_room(self, house: str, room: str):
        super().del_under_child(house, room)
        self.refresh()

    def toggle_silent(self, house: str, room: str):
        house_node = self.root.children[self.get_node_index(self.root, house)]
        room_node = house_node.children[self.get_node_index(house_node, room)]
        room_node.data.silent = not room_node.data.silent
        self.refresh()

    def change_house_name(self, house: str, name: str):
        super().change_name_parent(house, name)

    def change_house_data(self, house: str, param: str, value: str):
        super().change_data_parent(house, param, value)

    def change_room_name(self, house: str, room: str, name: str):
        super().change_name_child(house, room, name)

    def change_room_data(self, house: str, room: str, param: str, value: str):
        super().change_data_child(house, room, param, value)

    def increase_pending(self, house: str, room: str):
        current_pending = int(super().get_data_child(house, room, "pending"))
        super().change_data_child(house, room, "pending", str(current_pending + 1))
        self.refresh()
