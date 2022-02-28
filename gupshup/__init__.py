import sys
from .ui import Tui
from .src.server import Server

USAGE = """
# USAGE:
----------

for server:
gupshup server

for user:
gupshup <username>
"""


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "server":
            print("ok")
            server = Server()
            server.start_connection()
        else:
            app = Tui()
            app.run()
    else:
        print(USAGE)
