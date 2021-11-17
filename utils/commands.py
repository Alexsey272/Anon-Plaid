from aiogram import types

async def default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('help','Помощь'),
            types.BotCommand('account','Мой аккаунт'),
            types.BotCommand('terms','Правила'),
            types.BotCommand('commands','команды чата'),
            types.BotCommand('support','Служба поддержки'),
            types.BotCommand('settings',	'Настройки'),
            types.BotCommand('pay','Подписки'),
            types.BotCommand('about','О боте')
        ]
    )