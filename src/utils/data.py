from typing import Any, List

class Data:
    def __init__(self, type: str, *params: List[Any]):
        self.type = type
        self.params = params

