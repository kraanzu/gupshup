import sys
from .ui import Tui
from .src.server import Server

def main():
    if sys.argv[1].lower() == "server":
        server = Server()
        server.start_connection()
    else:
        app = Tui()
        app.run()
