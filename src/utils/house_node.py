class CustomNode:
    def __init__(self, type: str, icon: str, color="white") -> None:
        self.type = type
        self.icon = icon
        self.pending = 0
        self.silent = False
        self.color = color
        self.hidden = False

    def change_icon(self, new_icon: str) -> None:
        self.icon = new_icon

    def change_silence(self):
        self.silent = not self.silent

    def change_pending(self, count: int):
        self.pending += count

    def change_color(self, color: str):
        self.color = color
        return color
