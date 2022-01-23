from rich.text import TextType
from .custom_tree import CustomTree


class MemberList(CustomTree):
    def __init__(self, name: TextType) -> None:
        super().__init__(name, "members_root")

    async def add_rank(self, name: str) -> None:
        await super().add_under_root(name, "rank")

    async def add_user_to_rank(self, rank: str, user: str) -> None:
        await self.add_under_child(rank, user, "user")
