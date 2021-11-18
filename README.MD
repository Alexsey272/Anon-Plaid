![Crimson Plaid](https://i.imgur.com/BBeyWph.jpeg)

![https://img.shields.io/badge/Python-3.10.0-blue](https://img.shields.io/badge/Python-3.10.0-blue)
![https://img.shields.io/badge/Status-BETA-red](https://img.shields.io/badge/Status-BETA-red) ![https://img.shields.io/badge/Realese-0.3-red](https://img.shields.io/badge/Realese-0.3-red) [![https://img.shields.io/badge/Telegram-Bot-blue](https://img.shields.io/badge/Telegram-Bot-blue)](https://t.me/Crimson_plaid_bot) [![License](https://img.shields.io/badge/license-GPL-green)](LICENSE) [![Report Bugs!](https://badgen.net/badge/🐞%20Report%20/Bugs/red)](https://t.me/anochat_support)


# Анонимный чат Crimson Plaid    
Проект написанный на языке Python, с помощью библиотеки Aiogram.

* Поддержка обмена аудио, видео и голосовых сообщений с собеседником. 
* анкеты пользователей для лучшего подбора собеседника.
* специальные команды, для диалогов.

# Get started
* Установите зависимости
```
$ git clone https://github.com/Alexsey272/Anon-Plaid.git
$ cd Anon-Plaid
$ pip install -r requirements.txt
```
* Создать файл `.env` и укажите переменные окружения
```Python
TOKENT = token_bot
ADMINS = list_admins
BOT_OWNER = id_bot_owner
PAYMENTS = token_payments
YANDEX_API = yandex_api
REPORT = id_channel_reports
ERROR = id_channel_errors
DIALOG = id_channel_dialogs
```
* Запустить скрипт
`$ python main.py`

## Admin panel
Панель администратора, предоставляет возможность:
* Добавить/Удалить администратора
* Заблокировать/разблокировать пользователя
* Получить файл с логами
* Получить список администраторов

Вызвать панель администратора можно с помощью команды `/admpanel`.

![screenshot](https://i.imgur.com/hpZ222y.jpeg)

## Credits  
https://github.com/RenatYakublevich/AnonymChat- Anonymous chat is based on this project

## Author  
© 2021 Crimson Plaid
