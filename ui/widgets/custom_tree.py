from rich.text import TextType, Text
from textual.widgets import TreeControl, TreeClick, NodeID, TreeNode
from rich.console import RenderableType

from textual.reactive import Reactive
from src.utils import CustomNode


class CustomTree(TreeControl):

    has_focus = Reactive(False)

    def __init__(self, name: TextType, data: CustomNode):
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

    def get_node_index(self, parent: TreeNode, name: str) -> int:
        for index, node in enumerate(parent.children):
            if str(node.label) == name:
                return index
        return -1

    async def add_under_root(self, name: str, tag: CustomNode) -> None:
        await self.root.add(name, tag)

    async def add_under_child(self, child: str, name: str, tag: CustomNode) -> None:
        for node in self.root.children:
            if str(node.label) == child:
                if name not in node.children:
                    await node.add(name, tag)
                break

    def del_under_root(self, name: str):
        index = self.get_node_index(self.root, name)

        self.root.children.pop(index)
        self.root.tree.children.pop(index)
        self.refresh()

    def del_under_child(self, parent: str, child: str):
        parent_index = self.get_node_index(self.root, parent)
        parent_node = self.root.children[parent_index]
        child_index = self.get_node_index(parent_node, child)

        parent_node.children.pop(child_index)
        parent_node.tree.children.pop(child_index)

    def change_data(self, param: str, data: str):
        self.data[param] = data
        self.refresh()
