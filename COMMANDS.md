***Note:*** </br>
**(some_text)** is a  mandatory field </br>
**[some_text]** is an optional field

## Commands for HOME
<pre>
Note: name here, in some cases, is optional because you can use these commands in different ways
like when you are in 'HOME/general' you will write        -- /ban jon_doe
but if you are currently in jon_doe's chat you will write -- /ban
</pre>

| Command      | Action                                                                                               |Syntax                      |
|:------------:|:-----------------------------------------------------------------------------------------------------|----------------------------|
| add_house    |  Creates a brand new house if there is not one in the server, of which, you are the owner            | /add_house (name)          |
| join         |  Allows you to join a house with the name you passed, if there is one                                | /join (name)               |
| add_room     |  Allows you to add a user with the given user in the direct chat                                     | /add_room (name)           |
| ban          |  Allows you to ban a user such that the user will not be able to text you                            | /ban [name]                |
| unban        |  Allows you to unban a user, if there is one                                                         | /unban (username)          |
| clear_chat   |  Allows you to clear the chat with the user the user will stay in direct chats                       | /clear_chat [name]         |
| del_room     |  This is a bit different from clear chat, in this the user option will be removed from direct chat   | /del_chat [name]           |
| archive     |  This is a bit different from del_room. delete_room deletes the chat and hides the room from `HOME` but archive does  not delete the chat| /archive [name]           |
| toggle_silent|  You won't hear a notification bell if this user texts you                                           | /toggle_silent [name]      |


## Commands for Houses

Note: commands are executed only if the user executing them has a minimum threshold of the required power (except bye and clear_chat)
There are two types of houses
- open: Anyone can join the house
- private: A request is sent to the owner of the house
<pre>
1 - Only available in private Houses
</pre>

| Command             | Action                                                                                               |  Syntax                               |
|:-------------------:|:-----------------------------------------------------------------------------------------------------|-------------------------------------- |
| clear_chat          |  Allows you to clear the chat with the user the user will stay in direct chats                       | /clear_chat                           |
| add_room            |  Adds a new room to the house                                                                        | /add_room (name) [icon]               |
| del_room            |  Deletes the specified room                                                                          | /del_room (name)                      |
| mute                |  Mutes the specified user.. his text will reach nobody                                               | /mute (name)                          |
| unmute              |  Unmutes a muted user                                                                                | /unmute (name)                        |
| ban                 |  Allows you to ban a user so they won't be able to enter the house                                   | /ban (name)                           |
| unban               |  Allows you to unban a banned user                                                                   | /unban
(username)                     |
| kick                |  Kick the user from the house                                                                        | /kick (name)                          |
| toggle_type         |  Toggle's the group type between open and private                                                    | /toggle_type                          |
| accept<sup>1</sup>  |  Accept a user's request to join the group                                                           | /accept (name)                        |
| reject<sup>1</sup>  |  Reject a user's request to join the group                                                           | /reject (name)                        |
| add_rank            |  Add a new rank in the house                                                                         | /add_rank (name) [color] [icon]       |
| del_rank            |  Delete a rank from the house                                                                        | /del_rank  (name)                     |
| assign_rank         |  Assign a rank to a user                                                                             | /assign_rank (name) (rank)            |
| change_rank_color   |  Change a rannk's color                                                                              | /change_rank_color (rank) (color)     |
| change_rank_icon    |  Change a rank's icon                                                                                | /change_rank_icon  (rank) (icon)      |
| change_rank_name    |  Change a rank's name                                                                                | /change_rank_name  (rank) (name)      |
| change_room_name    |  Change a room's name                                                                                | /change_room_name  (room) (name)      |
| change_room_icon    |  Change a room's icon                                                                                | /change_room_icon  (room) (icon)      |
| change_command_power|  Change a command's power level                                                                      | /change_command_power (commad) (power)|
| bye                 |  Leave the house                                                                                     | /bye|
gupshup on  main [ 1 ] is 📦 v0.1.0 via v3.10.2
 vim COMMANDS.md
gupshup on  main [ 1 ] is 📦 v0.1.0 via v3.10.2  9s
 cat COMMANDS.md
***Note:*** </br>
**(some_text)** is a  mandatory field </br>
**[some_text]** is an optional field

## Commands for HOME
<pre>
Note: name here, in some cases, is optional because you can use these commands in different ways
like when you are in 'HOME/general' you will write        -- /ban jon_doe
but if you are currently in jon_doe's chat you will write -- /ban
</pre>

| Command      | Action                                                                                               |Syntax                      |
|:------------:|:-----------------------------------------------------------------------------------------------------|----------------------------|
| add_house    |  Creates a brand new house if there is not one in the server, of which, you are the owner            | /add_house (name)          |
| join         |  Allows you to join a house with the name you passed, if there is one                                | /join (name)               |
| add_room     |  Allows you to add a user with the given user in the direct chat                                     | /add_room (name)           |
| ban          |  Allows you to ban a user such that the user will not be able to text you                            | /ban [name]                |
| unban        |  Allows you to unban a user, if there is one                                                         | /unban (username)          |
| clear_chat   |  Allows you to clear the chat with the user the user will stay in direct chats                       | /clear_chat [name]         |
| del_room     |  This is a bit different from clear chat, in this the user option will be removed from direct chat   | /del_chat [name]           |
| archive     |  This is a bit different from del_chat. Delete chat deletes the chat and hides the room from `HOME` but archive does  not delete the chat| /del_chat [name]           |
| toggle_silent|  You won't hear a notification bell if this user texts you                                           | /toggle_silent [name]      |


## Commands for Houses

Note: commands are executed only if the user executing them has a minimum threshold of the required power (except bye and clear_chat)
There are two types of houses
- open: Anyone can join the house
- private: A request is sent to the owner of the house
<pre>
1 - Only available in private Houses
</pre>

| Command             | Action                                                                                               |  Syntax                               |
|:-------------------:|:-----------------------------------------------------------------------------------------------------|-------------------------------------- |
| clear_chat          |  Allows you to clear the chat with the user the user will stay in direct chats                       | /clear_chat                           |
| add_room            |  Adds a new room to the house                                                                        | /add_room (name) [icon]               |
| del_room            |  Deletes the specified room                                                                          | /del_room (name)                      |
| mute                |  Mutes the specified user.. his text will reach nobody                                               | /mute (name)                          |
| unmute              |  Unmutes a muted user                                                                                | /unmute (name)                        |
| ban                 |  Allows you to ban a user so they won't be able to enter the house                                   | /ban (name)                           |
| unban               |  Allows you to unban a banned user                                                                   | /unban (username)                     |
| kick                |  Kick the user from the house                                                                        | /kick (name)                          |
| toggle_type         |  Toggle's the group type between open and private                                                    | /toggle_type                          |
| accept<sup>1</sup>  |  Accept a user's request to join the group                                                           | /accept (name)                        |
| reject<sup>1</sup>  |  Reject a user's request to join the group                                                           | /reject (name)                        |
| add_rank            |  Add a new rank in the house                                                                         | /add_rank (name) [color] [icon]       |
| del_rank            |  Delete a rank from the house                                                                        | /del_rank  (name)                     |
| assign_rank         |  Assign a rank to a user                                                                             | /assign_rank (name) (rank)            |
| change_rank_color   |  Change a rannk's color                                                                              | /change_rank_color (rank) (color)     |
| change_rank_icon    |  Change a rank's icon                                                                                | /change_rank_icon  (rank) (icon)      |
| change_rank_name    |  Change a rank's name                                                                                | /change_rank_name  (rank) (name)      |
| change_room_name    |  Change a room's name                                                                                | /change_room_name  (room) (name)      |
| change_room_icon    |  Change a room's icon                                                                                | /change_room_icon  (room) (icon)      |
| change_command_power|  Change a command's power level                                                                      | /change_command_power (commad) (power)|
| bye                 |  Leave the house                                                                                     | /bye|

