from random import choice

"""
Message templates for special commands `welcome`, `mute` and `kick`
"""


def welcome_message(user: str) -> str:
    return choice(
        [
            f"welcome {user}, we hope you bought some snacks",
            f"A wild {user} appeared",
            f"{user} just slid into the house",
            f"{user} just crashed into the house",
            f"Everyone welcome our newest member {user}",
            f"Finally! you made it here, {user}",
            f"{user} just showed up out of nowhere!",
            f"Welcome to the party, {user}",
        ]
    )


def mute_message() -> str:
    return choice(
        [
            "Keep calm and listen to other people",
            "Do you even realize what your are saying? Stay quiet",
            "Your messages are gonna vanish into thin air ",
            "Know your place and keep your mouth shut",
            "Your dumb is the very reason that you got muted",
            "They think you say stupid things and now you are muted ...RIP",
        ]
    )


def kick_message(house: str) -> str:
    return choice(
        [
            f"Know your place fool, you were kicked out from {house}",
            f"Members of {house} thought you are not worthy and kicked you out",
            f"You were shamelessly kicked out from {house}",
        ]
    )
