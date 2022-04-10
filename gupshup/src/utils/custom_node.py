class CustomNode:
    """
    A data class for Node information
    """

    def __init__(self, type: str, icon: str, color="white") -> None:
        self.type = type
        self.icon = icon
        self.pending = "0"
        self.silent = False
        self.color = color
        self.hidden = False
