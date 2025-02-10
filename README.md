<br/>

<div align="center">
    <img src="https://img.shields.io/static/v1?label=discord help&message=qxh&color=7289d9" />
</div>

<br/>

## TwoDifferentWorlds
A Discord bot base designed for big (and organized) Discord bots.


<br/>

```python
from models.client import Void

bot = Void()
token = bot.config.get("bot", "token")
>>> "your_token_here"
```

## Translations
Translations are stored in the `./src/translations` folder. To manage supported translations, add the language code to the `./src/config/data.cfg` file under the `translation_locales` key. The default language is `en` (English).
Additional codes are available [here](https://www.science.co.il/language/Locale-codes.php). To add support for a new language, create a JSON file in the `./src/translations` folder with the language code as the file name. Example: `./src/translations/de.json`. The JSON file can be empty, it will be initialized and read from automatically.

## Patreon-Only Features
If you want to implement Patreon-only features, set up the Patreon Discord integration which will create a Patreon-only role inside your bot's support Discord server (configured via `support_server_id` key). Once a user subscribes to your Patreon and is in your Discord server, they will be given the Patreon-only role (configured via `patreon_role_id`). Now you can use the Patreon-only check inside `./src/private/common.py` to check if the current server (more specifically the server owner) is a subscriber.

## Testing
Tests are stored in the `./src/tests` folder. To run the tests, use the command `pytest`. Keep in mind that the file prefix and any function prefix must be `test_` for the test to be recognized.

## Command Structure
This bot uses a per-file command structure. This means that each command is stored in its own file in order to not clutter all commands inside a single file, making everything more unorganized. Instead, treat the files and folders as a command tree, where each folder is a category and each file is a command. The command tree is stored in the `./src/commands` folder. Example (relative to `./src/commands/example`):

- dadjoke.py | **/example dadjoke [args]**
- ansitest.py | **/example ansitest [args]**
- index.py
- subgroup/ ->
    - index.py
    - some_command.py | **/example subgroup some_command [args]**

> **Note**
> Files inside the `etc` directory are considered being anything else than a command, like a Modal or a View. Those are ignored by the command registering system.

Notice how there's an `index.py` file in every folder. The `./index.py` file (not the one in `subgroup/`) is the Cog that holds all event listeners and variables for this specific command category. Everything you initialize there is globally usable within that category, as the class instance is passed along every command. The `./subgroup/index.py` file is just the group that is necessary to let Discord register the subcategory. If you wish to not layer your commands, don't use subgroups at all and change the class type in the first `index.py` to `Cog` instead of `GroupCog`. That way you can make commands like this: **/some_command [args]**.


<br/>
<br/>

## Requirement Installation and Running
-   $ `pip install -r requirements.txt`
-   $ `python src/main.py`
