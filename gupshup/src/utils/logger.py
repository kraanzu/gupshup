from datetime import datetime
from rich.console import Console

console = Console()


def time_now():
    return datetime.now().time().strftime("%X")


def colored(text, color):
    return f"[{color}]{text}[/{color}]"


def info(message):
    console.print(f"{time_now()} [{colored('INFO', 'blue')}] | {message}")


def warn(message):
    console.print(f"{time_now()} [{colored('WARN', 'yellow')}] | {message}")


def err(message):
    console.print(f"{time_now()} [{colored('ERR ', 'red')}] | {message}")


def debug(message):
    console.print(f"{time_now()} [{colored('DBG ', 'cyan')}] | {message}")
