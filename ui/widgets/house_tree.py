from os import get_terminal_size
from rich.panel import Panel
from rich.box import SIMPLE
from rich.text import TextType, Text
from rich.console import RenderableType
from textual.widgets import TreeNode, NodeID

from .custom_tree import CustomTree
from src.utils import CustomNode


class HouseTree(CustomTree):
    def __init__(self) -> None:
        name = Text("House Tree", style="bold red")
        super().__init__(name, CustomNode(type="house_root", icon=""))

    def render_node(self, node: TreeNode) -> RenderableType:
        return self.render_tree_label(
            node,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    def render_tree_label(
        self,
        node: TreeNode,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ):

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = Text(node.label) if isinstance(node.label, str) else node.label
        if is_hover:
            label.stylize("bold red" if node.data.type == "house_root" else "magenta")

        icon = node.data.icon
        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)

        return icon_label

    async def add_house(self, name: str) -> None:
        await super().add_under_root(name, CustomNode(type="house", icon="ﳐ"))
        await self.add_room(name, "general")

    async def add_room(self, house: str, name: str) -> None:
        await self.add_under_child(house, name, CustomNode(type="room", icon="ﴘ"))

    def del_house(self, name: str):
        super().del_under_root(name)
