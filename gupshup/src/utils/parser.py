import os
from configparser import ConfigParser

DEFAULTS = {
    "house_tree_icon": "",
    "house_tree_root": "red",
    "member_tree_root": "red",
    "member_tree_icon": " ",
    "header_bg": "black",
    "header_fg": "magenta",
    "banner_fg": "blue",
    "branch_hover": "red",
    "input_box_border": "blue",
    "input_placeholder": "Say something here...",
}


class Parser(ConfigParser):
    """
    A class to parse the currenty set options in the settings menu
    """

    file_path = os.path.join(os.path.expanduser("~"), ".config", "gupshup", "theme.ini")

    def __init__(self) -> None:
        super().__init__()
        try:
            if not self.read(self.file_path):
                with open(self.file_path, "w"):
                    pass

                self._create_user_config()
        except:
            self._create_user_config()

    def _create_user_config(self) -> None:
        try:
            home = os.path.expanduser("~")
            os.mkdir(os.path.join(home, ".config", "gupshup"))
        except FileExistsError:
            pass

        self.read(self.file_path)
        self.add_section("theme")
        for setting, value in DEFAULTS.items():
            self.set_data(setting, value)

        self._write_to_file()
        with open(self.file_path, "a") as f:
            f.write(
                "; available colors: https://rich.readthedocs.io/en/stable/appendix/colors.html"
            )

    def _write_to_file(self) -> None:
        with open(self.file_path, "w") as fp:
            self.write(fp)

    def set_data(self, data: str, val: str) -> None:
        super().set("theme", data, val)
        self._write_to_file()

    def get_data(self, data: str) -> str:
        return super().get("theme", data)


if __name__ == "__main__":
    parser = Parser()
