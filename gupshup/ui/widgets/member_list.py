from rich.text import Text
from rich.console import RenderableType
from textual.widgets import TreeNode

from .custom_tree import CustomTree
from ...src.utils import CustomNode, Parser


class MemberList(CustomTree):
    """
    A Class to show a tree-like structure of members of a group and their respective ranks
    """

    def __init__(self) -> None:
        theme = Parser()
        name = Text("Members", style=theme.get_data("member_tree_root"))
        super().__init__(
            name,
            CustomNode(
                type="member_root", icon=theme.get_data("member_tree_icon"), color="red"
            ),
        )

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Custom rendering of node
        """
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
        Custom highlighting for different parts of the node
        """

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = Text(node.label) if isinstance(node.label, str) else node.label
        label.stylize(node.data.color)

        if is_hover:
            label.stylize("bold red" if node.data.type == "member_root" else "magenta")

        icon = node.data.icon
        icon_label = (
            Text(
                f"{icon} ",
                no_wrap=True,
                overflow="ellipsis",
            )
            + label
        )
        icon_label.apply_meta(meta)

        return icon_label

    async def add_rank(self, name: str) -> None:
        await super().add_under_root(name, CustomNode(type="rank", icon=""))

    async def add_user_to_rank(self, rank: str, user: str) -> None:
        """
        Assign the user a rank
        """

        await self.add_under_child(rank, user, CustomNode(type="member", icon=""))

    async def del_from_rank(self, rank: str, member: str) -> None:
        """
        Deletes the user from the rank
        """

        super().del_under_child(rank, member)

    async def del_rank(self, rank: str) -> None:
        super().del_under_root(rank)

    async def change_rank_data(self, rank: str, param: str, value: str) -> None:
        """
        Changes rank data like icon or color
        """

        super().change_data_parent(rank, param, value)

    async def change_rank_name(self, rank: str, name: str) -> None:
        super().change_name_parent(rank, name)
