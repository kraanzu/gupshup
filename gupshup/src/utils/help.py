def colored(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


seperator = f"{colored('─' * 50, 'bold dim black')}"


def make_list(cmds: list[list[str]]):
    res = ""
    for name, desc, syntax in cmds:
        res += (
            "\n"
            + f"{colored('name:', 'yellow')} {name}"
            + "\n"
            + f"{colored('desc:', 'yellow')} {desc}"
            + "\n"
            + f"{colored('syntax:', 'yellow')} {syntax}"
            + "\n"
        )

    return res


home_cmds = [
    [
        "add_house",
        "Creates a brand new house if there is not one in the server, of which, you are the owner",
        "/add_house (name)",
    ],
    [
        "join",
        "Allows you to join a house with the name you passed, if there is one",
        "/join (name)",
    ],
    [
        "add_room",
        "Allows you to add a user with the given user in the direct chat",
        "/add_room (name)",
    ],
    [
        "ban",
        "Allows you to ban a user such that the user will not be able to text you",
        "/ban [ name ]",
    ],
    [
        "unban",
        "Allows you to unban a user, if there is one",
        "/unban (username)",
    ],
    [
        "clear_chat",
        "Allows you to clear the chat with the user the user will stay in direct chats",
        "/clear_chat [ name ]",
    ],
    [
        "del_room",
        "This is a bit different from clear chat, in this the user option will be removed from direct chat",
        "/del_chat [ name ]",
    ],
    [
        "archive",
        "This is a bit different from del_room. "
        + "\n"
        + "      delete_room deletes the chat and hides the room from `HOME`"
        + "\n"
        + "      but archive does  not delete the chat",
        "/archive [name]",
    ],
    [
        "toggle_silent",
        "You won't hear a notification bell if this user texts you",
        "/toggle_silent [ name ]",
    ],
]


house_cmds = [
    [
        "clear_chat",
        "Allows you to clear the chat with the user the user will stay in direct chats",
        "/clear_chat",
    ],
    [
        "add_room",
        "Adds a new room to the house",
        "/add_room (name) [ icon ]",
    ],
    [
        "del_room",
        "Deletes the specified room",
        "/del_room (name)",
    ],
    [
        "mute",
        "Mutes the specified user.. his text will reach nobody",
        "/mute (name)",
    ],
    [
        "ban",
        "Allows you to ban a user so they won't be able to enter the house",
        "/ban (name)",
    ],
    [
        "unban",
        "Allows you to unban a banned user",
        "/unban (username)",
    ],
    [
        "kick",
        "Kick the user from the house",
        "/kick (name)",
    ],
    [
        "toggle_type",
        "Toggle's the group type between open and private",
        "/toggle_type",
    ],
    [
        "accept(1)",
        "Accept a user's request to join the group",
        "/accept (name)",
    ],
    [
        "reject(1)",
        "Reject a user's request to join the group",
        "/reject (name)",
    ],
    [
        "add_rank",
        "Add a new rank in the house",
        "/add_rank (name) [ color ] [ icon ]",
    ],
    [
        "del_rank",
        "Delete a rank from the house",
        "/del_rank (name)",
    ],
    [
        "assign_rank",
        "Assign a rank to a user",
        "/assign_rank (name) (rank)",
    ],
    [
        "rank_info",
        "Displays a rank's info",
        "/rank_info (rank)",
    ],
    [
        "rank_levels",
        "Displays all rank's with their power levels",
        "/rank_levels",
    ],
    [
        "change_rank_color",
        "Change a rannk's color",
        "/change_rank_color (rank) (color)",
    ],
    [
        "change_rank_icon",
        "Change a rank's icon",
        "/change_rank_icon (rank) (icon)",
    ],
    [
        "change_rank_name",
        "Change a rank's name",
        "/change_rank_name (rank) (name)",
    ],
    [
        "change_rank_power",
        "Change a rank's power",
        "/change_rank_power (rank) (power)",
    ],
    [
        "add_rank_desc",
        "Add a rank's description",
        "/add_rank_desc (rank) (desc)",
    ],
    [
        "change_room_name",
        "Change a room's name",
        "/change_room_name (room) (name)",
    ],
    [
        "change_room_icon",
        "Change a room's icon",
        "/change_room_icon (room) (icon)",
    ],
    [
        "change_command_power",
        "Change a command's power level",
        "/change_command_power (commad) (power)",
    ],
    [
        "destroy",
        "Destroys the house",
        "/destroy",
    ],
    [
        "bye",
        "Leave the house",
        "/bye",
    ],
]

HELP_TEXT = f"""


{colored("Welcome to Gupshup ...","hot_pink3")}
{colored("Gupshup is TUI (Text User Interface) chat application with a great responsive UI and feel!" , "hot_pink3")}

{seperator}

Some basic navigation:
    - use {colored("ctrl+j", "bold blue")} to move to next room
    - use {colored("ctrl+k", "bold blue")} to move to prev room
    - use {colored("ctrl+l", "bold blue")} to move to next house
    - use {colored("ctrl+h", "bold blue")} to move to prev house

{seperator}

{colored("Note", "blue")}:
( some_text ) is a mandatory field
[ some_text ] is an optional field

{seperator}

{colored("Commands for HOME", "blue")}

Note: name here, in some cases, is optional because you can use these commands in different ways
like when you are in 'HOME/general' you will write        -- /ban jon_doe
but if you are currently in jon_doe's chat you will write -- /ban

{make_list(home_cmds)}

{seperator}
{seperator}

{ colored( "Commands for Houses", "blue" ) }
{colored("Note", "yellow")}: commands are executed only if the user executing them has a minimum threshold
of the required power (except bye and clear_chat) There are two types of houses

- open: Anyone can join the house
- private: A request is sent to the owner of the house

{colored("1 - Only available in private Houses", "orange1")}

{make_list(house_cmds)}

{seperator}
{seperator}

{colored("Additional: ", "orange1")}
available colors: https://rich.readthedocs.io/en/stable/appendix/colors.html

{seperator}

{colored("I hope you like this little project :heart:", "hot_pink3")}
{colored("-- kraanzu", "light_steel_blue")}

"""
