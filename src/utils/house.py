class House:
    def __init__(self, name: str, king: str):
        self.name = name
        self.king = king
        self.rooms = ['general']
        self.members = [king]
        self.member_ranks = {king: "king"}
        self.banned_users = []
        self.muted_users = []
        self.bot_binds = []

    def add_room(self, name: str) -> None:
        self.rooms += name,

    def del_room(self , name: str) -> None:
        self.rooms.remove(name)

    def ban_user(self, name: str) -> None:
        self.banned_users += name,

