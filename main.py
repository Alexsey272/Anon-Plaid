from aiogram import executor
from loader import dp
import handlers
from utils.notify import on_startup_notify
from utils.commands import default_commands

async def on_startup(dispatcher):

    await on_startup_notify(dispatcher)
    
    await default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup )
