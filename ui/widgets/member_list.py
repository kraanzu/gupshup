from rich.text import Text, TextType
from rich.console import RenderableType

from textual.widgets import TreeNode
from .custom_tree import CustomTree
from src.utils import CustomNode


class MemberList(CustomTree):
    def __init__(self) -> None:
        name = Text("Members", style="bold red")
        super().__init__(name, CustomNode(type="member_root", icon=""))

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
        label.stylize(node.data.color)

        if is_hover:
            label.stylize("bold blue" if node.data.type == "member_root" else "magenta")

        icon = node.data.icon
        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)

        return icon_label

    async def add_rank(self, name: str) -> None:
        await super().add_under_root(name, CustomNode(type="rank", icon="R"))
        self.refresh()

    async def add_user_to_rank(self, rank: str, user: str) -> None:
        await self.add_under_child(rank, user, CustomNode("type=member", icon="m"))
        self.refresh()

    async def del_from_rank(self, rank: str, member: str):
        super().del_under_child(rank, member)
        self.refresh()

    async def del_rank(self, rank: str):
        super().del_under_root(rank)
        self.refresh()

    async def change_rank_data(self, rank: str, param: str, value: str):
        super().change_data_parent(rank, param, value)
        self.refresh()

    async def change_rank_name(self, rank: str, name: str):
        super().change_name_parent(rank, name)
