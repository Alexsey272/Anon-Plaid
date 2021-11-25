![Crimson Plaid](https://i.imgur.com/BBeyWph.jpeg)

![https://img.shields.io/badge/Python-3.8.0-blue](https://img.shields.io/badge/Python-3.8.0-blue)
![https://img.shields.io/badge/Status-BETA-red](https://img.shields.io/badge/Status-BETA-red) ![https://img.shields.io/badge/Realese-0.3-red](https://img.shields.io/badge/Realese-0.3-red) [![https://img.shields.io/badge/Telegram-Bot-blue](https://img.shields.io/badge/Telegram-Bot-blue)](https://t.me/Crimson_plaid_bot) [![License](https://img.shields.io/badge/license-GPL-green)](LICENSE) [![Report Bugs!](https://badgen.net/badge/🐞%20Report%20/Bugs/red)](https://t.me/anochat_support)


# Anonymous Crimson Plaid Chat 
The project is written in Python, using the Aiogram library.

* Support for the exchange of audio, video and voice messages with the interlocutor. 
* user profiles for the best selection of the interlocutor.
* special commands for dialogs.

# Get started
* Install dependencies
```
$ git clone https://github.com/Alexsey272/Anon-Plaid.git
$ cd Anon-Plaid
$ pip install -r requirements.txt
```
* Create a `.env` file and specify the environment variables
```Python
#The bot token that you received from BotFather
TOKENT = <token_bot>
#ID of all administrators
ADMINS = <list_admins>
#ID of the bot owner
BOT_OWNER = <id_bot_owner>
#Channel ID for user complaints
REPORT = <id_channel_reports>
#Error channel ID
ERROR = <id_channel_errors>
#Channel ID for user messages
DIALOG = <id_channel_dialogs>
```
* Run the script
`$ python main.py`

## To-Do
- [ ] Rooms by interests
- [ ] Multilingualism
- [ ] Adding a description and age
- [ ] Personal dialogues
- [ ] Ability to delete the questionnaire
- [ ] registration menu
- [ ] Modify the admin panel

## Admin panel
The admin panel, provides the ability to:
* Add/Remove the administrator
* Block/unblock the user
* Get a file with logs
* Get a list of administrators
* Add a subscription to a user

You can open the admin panel using the command `/admpanel.`

![screenshot](https://i.imgur.com/hpZ222y.jpeg)

## Credits  
https://github.com/RenatYakublevich/AnonymChat - Anonymous chat is based on this project

## Author  
© 2021 Crimson Plaid
