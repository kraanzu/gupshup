from textual.widget import Widget
from textual.widgets import TreeControl, TreeNode
from rich.console import RenderableType
from rich.text import Text
from ...src.utils import Message


class ChatScreen(TreeControl):
    """
    A screen for providing chats
    """

    def __init__(self, name: str = ""):
        super().__init__(name, name)
        self.chats = ""
        self._tree.hide_root = True

    def render_node(self, node: TreeNode) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = Text.from_markup(str(node.label))
        if node.id == self.hover_node:
            label.append(" <=")
            label.stylize("bold")

        label.apply_meta(meta)
        return label

    async def clear_chat(self):
        self.root.children.clear()
        self.root.tree.children.clear()
        self.refresh()

    async def push_text(self, message: Message) -> None:
        if not self.root.expanded:
            await self.root.expand()

        msg = f"{message.sender}: {message.text}"
        self.chats += f"\n{message.sender}: {message.text}"
        await self.root.add(msg, "message")
        self.refresh()
