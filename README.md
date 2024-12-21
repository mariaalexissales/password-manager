# password-manager
 personal password manager bc i'm tired of paying for services


# How to use
| Command | Description | Example Usage |
|---------|-------------|---------------|
|`--init` | Initializes the database and the vault encryption key | `python3 main.py --init`|
|`--add`  | Adds your passed in app, username, and password to the vault | `python3 main.py --add [app] [username] [password]`|
|`--get`  | Grabs the password from the passed in app and username | `python3 main.py --get [app] [username]`|
|`--list` | Returns the entire list of apps and usernames | `python3 main.py --list` |
