from textual.widgets import TreeControl, TreeClick


class HouseTree(TreeControl):
    def __init__(self, name: str) -> None:
        super().__init__(name, "root")

    async def add_house(self, name: str) -> None:
        await self.root.add(name, "house")

    async def handle_tree_click(self, message: TreeClick):
        await message.node.toggle()
