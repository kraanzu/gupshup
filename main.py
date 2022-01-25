from ui import Tui
import sys
from src.server import Server

if sys.argv[1].lower() == "server":
    server = Server()
    server.start_connection()
else:
    app = Tui()
    app.run()
