from rich.text import TextType
from textual.widgets import TreeControl, TreeClick


class CustomTree(TreeControl):
    def __init__(self, name: TextType, tag: str):
        super().__init__(name, tag)

    async def add_under_root(self, name: str, tag: str) -> None:
        await self.root.add(name, tag)

    async def add_under_child(self, child: str, name: str, tag: str) -> None:
        for node in self.root.children:
            if str(node.label) == child:
                await node.add(name, tag)
                break

    def del_under_root(self, name: str):
        for child in self.root.children:
            if str(child.label) == name:
                to_del = child
                break

        del to_del
        self.refresh()

    async def handle_tree_click(self, _: TreeClick) -> None:
        pass
