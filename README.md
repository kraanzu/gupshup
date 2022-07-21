# Gupshup

Gupshup is TUI (Text User Interface) chat application with a great UI and feel! </br>
It implements various features as modern chat applications
such as ranking systems and special commands. </br>
see [here!](https://github.com/kraanzu/gupshup/blob/main/COMMANDS.md) </br>

It is good for now but I'll add more features to it :) </br>
There is a screenshot of the application attached below which will make it easier for you to understand the concept.

And also, It is built on top of [textual](https://github.com/Textualize/textual) which provides the UI for the application</br>
Shoutouts to [@willmcgugan](https://github.com/willmcgugan) for such a great library!

# Installation

***Note:*** Termtype needs python version ^3.10</br>
***Note:*** The default icons used in the app are a part of [Nerdfonts](https://www.nerdfonts.com/) </br>
***Note:*** This might not work on windows as intended but windows support is in pipeline and textual is working on it!

## One Liner
```bash
python3 -m pip install git+https://github.com/kraanzu/gupshup.git
```

## Or if you prefer Manual Installation
``` bash
git clone https://github.com/kraanzu/gupshup.git
cd gupshup
pip install .
```

# A screenshot of the application
![gupshup](https://user-images.githubusercontent.com/97718086/154282080-35ac8bc4-5c2e-4b16-a39a-a808bdd0aba1.png)

# Usage
A script be automatically generated to run it with a simple command gupshup in your terminal

**For spinning up a server:**
```bash
gupshup --server
```

**For connecting to a server:**
```bash
gupshup -u <username> 
```

**Note: You can add -q flag to supress notification sounds**
```bash
gupshup -u <username> -q 
```

# TODOs
- [ ] Add bots
- [ ] File Uploads

# Contribution
Always open to PRs :)

<p align="center"><a href="https://github.com/kraanzu/gupshup/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=License&message=MIT&logoColor=eceff4&logo=github&colorA=4c566a&colorB=88c0d0"/></a></p>
