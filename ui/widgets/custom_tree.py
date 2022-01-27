from rich.text import TextType, Text
from textual.widgets import TreeControl, TreeClick, NodeID, TreeNode
from rich.console import RenderableType

from textual.reactive import Reactive


class CustomTree(TreeControl):

    has_focus = Reactive(False)

    def __init__(self, name: TextType, data: RenderableType):
        super().__init__(name, data)

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = (
                "bold not dim red" if node.id == hover_node else "black"
            )
        self.refresh(layout=True)

    async def add_under_root(self, name: str, tag: RenderableType) -> None:
        await self.root.add(name, tag)

    async def add_under_child(self, child: str, name: str, tag: RenderableType) -> None:
        for node in self.root.children:
            if str(node.label) == child:
                if name not in node.children:
                    await node.add(name, tag)
                break

    def del_under_root(self, name: str):
        for child in self.root.children:
            if str(child.label) == name:
                to_del = child
                break

        del to_del
        self.refresh(layout=True)

    async def handle_tree_click(self, _: TreeClick) -> None:
        pass
