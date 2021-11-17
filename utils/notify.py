from aiogram import Dispatcher
import datetime
import logging
from data import config

async def on_startup_notify(dp: Dispatcher):
    for admin in config.ADMIN:
        try:
            await dp.bot.send_message(admin, datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S") + "\n[INFO] The bot is running")
        except Exception as err:
            logging.exception(err)