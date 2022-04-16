from .ui import Tui
from .src.server import Server

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-q", "--quiet", default=0, action="store_true", help="Supress notification sounds"
)
group = parser.add_mutually_exclusive_group()
group.add_argument("--server", action="store_true", help="Spins up a server")
group.add_argument("-u", "--user", type=str, help="Connects a user to the server")

args = parser.parse_args()


def main():
    if args.server:
        server = Server()
        server.start_connection()
    else:
        Tui.run(args.user, args.quiet)
