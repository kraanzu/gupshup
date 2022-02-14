from typing import Dict, List
from .message import Message
from .rank import Rank
from .message_templates import welcome_message, kick_message, mute_message
from collections import defaultdict


class HouseData:
    def __init__(
        self,
        name: str,
        rooms: set[str],
        room_icons: dict[str, str],
        ranks: dict[str, Rank],
        member_rank: dict[str, str],
    ):
        self.name = name
        self.rooms = rooms
        self.room_icons = dict(room_icons)
        self.ranks = dict(ranks)
        self.member_rank = dict(member_rank)


class House:
    def __init__(self, name: str, king: str) -> None:
        self.type = "open"
        self.name = name
        self.king = king
        self.rooms = {"general"}
        self.room_icons = dict()
        self.members = set([king])
        self.banned_users = set()
        self.muted_users = set()
        self.bot_binds = set()
        self.waiting_users = set()
        self.member_rank: Dict[str, str] = {king: "king"}
        self.ranks: Dict[str, Rank] = {
            "king": Rank("king", "red", float("inf"), icon=""),
            "pawn": Rank("pawn", icon=""),
        }
        self.room_icons["general"] = "ﴘ"
        self.required_power: Dict[str, float] = dict()

    def _is_allowed(self, action: str, user: str) -> bool:
        return self.ranks[self.member_rank[user]].power >= self.required_power.get(
            action, float("inf")
        )

    def add_to_waiting_list(self, user: str):
        self.waiting_users.add(user)

    def add_room(self, name: str) -> None:
        self.rooms.add(name)

    def del_room(self, name: str) -> None:
        self.rooms.remove(name)

    def ban_user(self, name: str) -> None:
        self.banned_users.add(name)

    def unban_user(self, name: str) -> None:
        self.banned_users.remove(name)

    def add_rank(self, rank: str):
        self.ranks[rank] = Rank(rank)

    def change_rank_color(self, rank: str, color: str):
        self.ranks[rank].color = color

    def change_rank_power(self, rank: str, power: float):
        self.ranks[rank].power = power

    def remove_member(self, member: str):
        self.members.remove(member)

    def mute_member(self, member: str):
        self.muted_users.add(member)

    def unmute_member(self, member: str):
        self.muted_users.remove(member)

    def toggle_type(self):
        self.type = "open" if self.type == "private" else "private"

    def _generate_house_data(self) -> HouseData:
        return HouseData(
            self.name, self.rooms, self.room_icons, self.ranks, self.member_rank
        )

    def add_member(self, user: str) -> List[Message]:
        self.members.add(user)
        x = [
            Message(
                action="add_house",
                data={"house": self._generate_house_data()},
                reciepents=[user],
            ),
            Message(
                action="push_text",
                sender="SERVER",
                house=self.name,
                room="general",
                text=welcome_message(user),
                reciepents=list(self.members),
            ),
            Message(
                action="add_user_rank",
                house=self.name,
                data={"rank": "pawn", "user": user},
                reciepents=list(self.members),
            ),
        ]
        self.member_rank[user] = "pawn"
        return x

    def action_mute(self, message: Message) -> List[Message]:
        user = message.text[6:].strip()
        if user in self.muted_users:
            return [message.convert(text="The user is already muted")]

        self.mute_member(user)
        return [
            message.convert(
                text=f"{user} was talking too much and thus was muted by {message.sender}",
                reciepents=list(self.members),
            ),
            message.convert(text=mute_message(), reciepents=[user]),
        ]

    def action_unmute(self, message: Message) -> List[Message]:
        user = message.text[8:].strip()
        if user not in self.muted_users:
            return [message.convert(text="The user is not muted")]

        self.unmute_member(user)
        return [
            message.convert(
                text=f"user {user} was unmuted by {message.sender}",
                reciepents=list(self.members),
            ),
        ]

    def action_kick(self, message: Message) -> List[Message]:
        member = message.text[6:].strip()

        if not member:
            raise ValueError

        if member not in self.members:
            return [message.convert(text="user not in the house")]

        x = [
            message.convert(
                text=f"User {member} was kicked out of the house",
                reciepents=list(self.members),
            ),
            message.convert(action="del_house", reciepents=[member]),
            message.convert(
                action="del_user_rank",
                reciepents=list(self.members),
                data={"rank": self.member_rank[member], "user": member},
            ),
        ]

        self.remove_member(member)
        del self.member_rank[member]
        self.members.remove(member)
        return x

    def action_toggle_type(self, message: Message) -> List[Message]:
        self.toggle_type()
        x = []
        for user in self.waiting_users:
            x.extend(self.add_member(user))

        self.waiting_users = set()

        return x + [
            Message(
                action="push_text",
                house=self.name,
                room="general",
                text=f"user {message.sender} toggled group's type [{self.type}]",
                reciepents=list(self.members),
            )
        ]

    def action_join(self, message: Message) -> List[Message]:
        if message.sender in self.banned_users:
            return [message.convert(text="you have been banned from this group")]

        if self.type == "open":
            return self.add_member(message.sender)

        self.add_to_waiting_list(message.sender),
        return [
            message.convert(
                text="Your request has been sent to the king of the house",
            ),
            message.convert(
                house=self.name,
                room="general",
                text=f"User {message.sender} has requested to join the group",
                reciepents=[self.king],
            ),
        ]

    def action_toggle_silent(self, message: Message) -> List[Message]:
        return [message.convert(action="toggle_silent")]

    def action_add_room(self, message: Message) -> List[Message]:
        room = message.text[10:]
        if room in self.rooms:
            return [message.convert(text="There is already a room with same name!")]

        self.add_room(room)
        return [
            message.convert(action="add_room", text=room, reciepents=list(self.members))
        ]

    def action_accept(self, message: Message) -> List[Message]:
        user = message.text[8:].strip()
        if user not in self.waiting_users:
            return [
                message.convert(
                    # house=self.name,
                    room="general",
                    text=f"no such user({user}) in the waiting list",
                    reciepents=[self.king],
                ),
            ]

        self.waiting_users.remove(user)
        return self.add_member(user)

    def action_ban_user(self, message: Message) -> List[Message]:
        user = message.text[10:].strip()
        if user in self.banned_users:
            return [message.convert(text=f"user {user} is already banned")]

        self.ban_user(user)
        return [
            message.convert(
                text=f"user {user} was banned by {message.sender}",
                reciepents=list(self.members),
            )
        ]

    def action_unban_user(self, message: Message) -> List[Message]:
        user = message.text[12:].strip()
        if user not in self.banned_users:
            return [message.convert(text=f"user {user} is not in the banned list")]

        self.unban_user(user)
        return [
            message.convert(
                text=f"user {user} was unbanned by {message.sender}",
                reciepents=list(self.members),
            )
        ]

    def action_del_room(self, message: Message) -> List[Message]:
        room = message.text[10:].strip()
        if room == "general":
            return [message.convert(text="you can't delete the general chat")]
        elif room not in self.rooms:
            return [message.convert(text=f"there is no room with the name {room}")]
        return [
            message.convert(action="del_room", room=room, reciepents=list(self.members))
        ]

    def action_destroy(self, message: Message):
        return [message.convert(action="del_house", reciepents=list(self.members))]

    def action_del_chat(self, message: Message):
        return [message.convert(action="del_chat")]

    def action_add_rank(self, message: Message):
        rank = message.text[10:].strip()
        if rank in self.ranks:
            return [message.convert(text="there is already a rank with same name")]

        self.ranks[rank] = Rank(rank)
        return [
            message.convert(
                action="add_rank", text=rank, reciepents=list(self.members)
            ),
        ]

    def action_del_rank(self, message: Message):
        rank = message.text[10:].strip()
        if rank not in self.ranks:
            return [message.convert(text="there is no such rank in this house")]
        if rank in ["king", "pawn"]:
            return [message.convert(text="You can't delete this rank")]
        return [
            message.convert(
                action="del_rank", text=rank, reciepents=list(self.members)
            ),
        ]

    def action_assign_rank(self, message: Message) -> List[Message]:
        param = message.text[13:].strip()
        user, rank = param.split(" ", 1)
        if user not in self.members:
            return [message.convert(text="no such user in the house")]

        prev_rank = self.member_rank[user]
        if prev_rank == rank:
            return [message.convert(text="this user already has this rank")]

        self.member_rank[user] = rank
        return [
            message.convert(
                action="del_user_rank",
                data={"rank": prev_rank, "user": user},
                reciepents=list(self.members),
            ),
            message.convert(
                action="add_user_rank",
                data={"rank": rank, "user": user},
                reciepents=list(self.members),
            ),
        ]

    def action_list_ranks(self, message: Message) -> List[Message]:
        return [message.convert(text=f"The ranks are: {', '.join(self.ranks)}")]

    def action_rank_info(self, message: Message) -> List[Message]:
        rank = message.text[11:].strip()
        if rank not in self.ranks:
            return [message.convert(text="No such rank in the house")]

        return [message.convert(text=self.ranks[rank].info)]

    def action_add_rank_info(self, message: Message) -> List[Message]:
        param = message.text[15:].strip()
        rank, info = param.split(" ", 1)
        if rank not in self.ranks:
            return [message.convert(text="No such rank in the house")]

        self.ranks[rank].info = info
        return []

    def action_change_rank_icon(self, message: Message) -> List[Message]:
        param = message.text[18:].strip()
        rank, icon = param.split(" ", 1)
        self.ranks[rank].icon = icon
        return [
            message.convert(
                action="change_rank_icon",
                data={"rank": rank, "icon": icon},
                reciepents=list(self.members),
            )
        ]

    def action_change_rank_name(self, message: Message) -> List[Message]:
        param = message.text[18:].strip()
        rank, name = param.split(" ", 1)
        return [
            message.convert(
                action="change_rank_name",
                data={"rank": rank, "name": name},
                reciepents=list(self.members),
            )
        ]

    def action_change_rank_color(self, message: Message) -> List[Message]:
        param = message.text[19:].strip()
        rank, color = param.split(" ", 1)
        self.ranks[rank].color = color
        return [
            message.convert(
                action="change_rank_color",
                data={"rank": rank, "color": color},
                reciepents=list(self.members),
            )
        ]

    def action_change_rank_power(self, message: Message) -> List[Message]:
        param = message.text[19:].strip()
        rank, power = param.split(" ", 1)
        self.ranks[rank].power = int(power)
        return [
            message.convert(
                text=f"rank {rank}'s power was set to {power}' by {message.sender}",
                reciepents=list(self.members),
            )
        ]

    def action_change_room_name(self, message: Message) -> List[Message]:
        name = message.text[18:].strip()
        return [
            message.convert(
                action="change_room_name",
                text=name,
                reciepents=list(self.members),
            )
        ]

    def action_change_room_icon(self, message: Message) -> List[Message]:
        name = message.text[18:].strip()
        print(message.text)
        return [
            message.convert(
                action="change_room_icon",
                text=name,
                reciepents=list(self.members),
            )
        ]

    def action_change_command_power(self, message: Message) -> List[Message]:
        param = message.text[21:].strip()
        command, power = param.split(" ", 1)
        self.required_power[command] = int(power)
        return [
            message.convert(
                text=f"command {command}'s power level was set to {power} by {message.sender}'",
                reciepents=list(self.members),
            )
        ]

    def action_bye(self, message: Message) -> List[Message]:
        member = message.sender
        self.members.remove(member)

        x = [
            message.convert(
                text=f"{member} left the group",
                reciepents=list(self.members),
            ),
            message.convert(action="del_house"),
            message.convert(
                action="del_user_rank",
                reciepents=list(self.members),
                data={"rank": self.member_rank[member], "user": member},
            ),
        ]

        del self.member_rank[member]
        return x

    def process_message(self, message: Message) -> List[Message]:
        if message.text[0] == "/":
            return self.process_special_message(message)
        else:
            if message.sender not in self.muted_users:
                return [message.convert(sender="self", reciepents=list(self.members))]
            return []

    def process_special_message(self, message: Message) -> List[Message]:
        action, *_ = message.text[1:].split(" ", 1)

        if action not in [
            "del_chat",
            "toggle_silent",
            "join",
            "bye",
        ] and not self._is_allowed(action, message.sender):
            return [
                message.convert(
                    text="Your current power level doesn't allow this action",
                )
            ]
        try:
            cmd = f"self.action_{action}(message)"
            print("special", cmd)
            return eval(cmd)

        except AttributeError:
            return [message.convert(text="[red]No such command[/red]")]

        except ValueError:
            return [message.convert(text="[red]invalid use of command![/red]")]
