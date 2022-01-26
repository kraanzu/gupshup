from rich.text import TextType
from .custom_tree import CustomTree

class HouseTree(CustomTree):
    def __init__(self) -> None:
        super().__init__("Houses", "house_root")

    async def add_house(self, name: str) -> None:
        await super().add_under_root(name, "house")
        await self.add_room(name, "general")

    async def add_room(self, house: str, name: str) -> None:
        await self.add_under_child(house, name, "room")

    def del_house(self, name: str):
        super().del_under_root(name)
