from .ui import Tui
from .src.server import Server
import socket

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-q", "--quiet", default=0, action="store_true", help="Supress notification sounds"
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--server", action="store_true", help="Spins up a server")
group.add_argument("-u", "--user", type=str, help="Connects a user to the server")

args = parser.parse_args()


def main():
    if args.server:
        server = Server()
        server.start_connection()
    else:
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.bind(("localhost", 5500))
            conn.close()

            print("Can't connect to the server. Is it running?")
            exit()

        except OSError:
            Tui.run(args.user, args.quiet)
