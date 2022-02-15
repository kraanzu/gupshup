class Rank:
    """
    A rank class for the ranking
    """

    def __init__(
        self, name: str, color: str = "white", power: float = 0, icon="R"
    ) -> None:
        self.name = name
        self.color = color
        self.power = power
        self.desc = "This rank doesn't have an info yet!"
        self.info = (
            f"name: {self.name}"
            + "\n"
            + f"power: {self.power}"
            + "\n"
            + f"desc: {self.desc}"
        )
        self.icon = icon
