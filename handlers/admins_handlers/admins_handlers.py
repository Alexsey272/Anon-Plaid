from loader import dp, db, bot
from aiogram import Bot, types
from FSM import *
import aiogram.utils.exceptions
from aiogram.types.message import ContentTypes
from keyboards import admin_menu
from data import config
from utils.logging import warning_log

@dp.message_handler(commands=['admpanel'])
async def send_message(message: types.Message):
    if db.admin_exists(message.from_user.id):
        await bot.send_message(message.from_user.id, f'*Панель администратора*\n\n*Счетчик пользователей:*\n_В боте зарегистрировано уже {int(db.count_user())} пользователей_\n\n_Выберите действие:_', reply_markup = admin_menu, parse_mode = "Markdown")


@dp.message_handler(commands=['message'])
async def send_message(message: types.Message):
    if db.admin_exists(message.from_user.id):
        await SendMessage.user.set()
        await message.answer(
            "*Укажи ID пользователя, которому хотите отправить сообщение*"
            "\n\n_Для отмены действия, отправьте слово 'Отмена'_",
            parse_mode="Markdown")
    else:
        await message.answer("⚠️ *Команда доступна только администраторам*", parse_mode="markdown")


@dp.message_handler(lambda message: message.text.isdigit(), state=SendMessage.user)
async def add_user_msg(message: types.Message, state: FSMContext):
    if not db.user_exists(message.text):
        await message.answer("*Пользователь с данным ID, не найден*", parse_mode="Markdown")
    else:
        async with state.proxy() as data:
            data['user'] = message.text

        await SendMessage.next()
        await message.answer("Введите сообщение для отправки", parse_mode="Markdown")


@dp.message_handler(lambda message: not message.text.isdigit(), state=SendMessage.user)
async def not_add_user_msg(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await message.answer("_Действие отменено_", parse_mode="Markdown")
    else:
        await message.answer("_ID пользователя должно состоять только из цифр, введите ID пользователя еще раз_",
                             parse_mode="Markdown")


@dp.message_handler(state=SendMessage.msg)
async def send_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
        msg = data['msg']

        await bot.send_message(data['user'], f"*Сообщение от администратора:*\n_{msg}_", parse_mode="Markdown")
        await state.finish()
        return await message.answer("✅ *Сообщение отправлено*", parse_mode="Markdown")


@dp.message_handler(commands=['allmsg'])
async def send_message(message: types.Message):
    if db.admin_exists(message.from_user.id):
        await AllMessage.msg.set()
        await message.answer(
            "*Что вы хотите разослать всем пользователям?*",
            parse_mode="Markdown")
    else:
        await message.answer("⚠️ *Команда доступна только администраторам*", parse_mode="markdown")


@dp.message_handler(content_types=ContentTypes.PHOTO, state=AllMessage.msg)
async def add_photo_report(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['msg'] = message.caption
            msg = data['msg']

            await message.photo[-1].download('photo_user/' + str(message.from_user.id) + 'spam.jpg')
            with open('photo_user/' + str(message.from_user.id) + 'spam.jpg', 'rb') as photo:
                for m in db.get_all_users():
                    await bot.send_photo(int(m[0]), photo, caption=f"*{msg}*", parse_mode="Markdown")

            await message.answer(
            "✅ *Рассылка завершена*",
            parse_mode="Markdown")
            await state.finish()
    except aiogram.utils.exceptions.BotBlocked:
    	await message.answer("😔 Собеседник заблокировал бота!")
    	db.delete_block_user(db.select_connect_with(message.from_user.id)[0], message.from_user.id, None)
    	await state.finish()
    	await start(message, state)


@dp.message_handler(content_types=ContentTypes.TEXT, state=AllMessage.msg)
async def add_user_msg(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['msg'] = message.text
            msg = data['msg']

            for m in db.get_all_users():
                await bot.send_message(int(m[0]), f"*{msg}*", parse_mode="Markdown")
            await state.finish()

            return await message.answer("✅ *Рассылка завершена*", parse_mode="Markdown")
    except aiogram.utils.exceptions.BotBlocked:
    	await message.answer("😔 Собеседник заблокировал бота!")
    	db.delete_block_user(db.select_connect_with(message.from_user.id)[0], message.from_user.id, None)
    	await state.finish()
    	await start(message, state)



@dp.message_handler(lambda message: message.text.isdigit(), state=Block.user)
async def add_black_list(message: types.Message, state: FSMContext):
    if not db.user_exists(message.text):
        await message.answer("*Пользователь с данным ID, не найден*", parse_mode="Markdown")
    else:
        if message.text != str(config.BOT_OWNER):
            async with state.proxy() as data:
                data['user'] = message.text

                await Block.next()
                await message.answer("_Укажите причину блокировки_", parse_mode="Markdown")
        else:
            await message.answer("*Невозможно заблокировать владельца чата*", parse_mode="Markdown")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Block.user)
async def not_add_black_list(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await message.answer("Действие отменено")
    else:
        return await message.answer("_ID пользователя должно состоять только из цифр, введите ID пользователя еще раз_",
                                    parse_mode="Markdown")


@dp.message_handler(state=Block.cause)
async def add_cause(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cause'] = message.text

        await Block.next()
        await message.answer("_На какое время пользователь будет заблокирован_", parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.isdigit(), state=Block.time)
async def add_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

        block_id = data['user']
        cause = data['cause']
        time = data['time']

        db.blocked_user(block_id)
        await message.answer(f"⛔ *Пользователь {block_id} заблокирован*", parse_mode="Markdown")
        await bot.send_message(block_id,
                               f"*Вас заблокировала администрация чата*\n_Срок: {time} дней_\n_Причина: {cause}_",
                               parse_mode="Markdown")
        await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit(), state=Block.time)
async def not_add_time(message: types.Message, state: FSMContext):
    return await message.answer("Укажите длительность блокировки цифрами")


@dp.message_handler(lambda message: message.text.isdigit(), state=Unblock.user)
async def Unblocked_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user'] = message.text
        unblock_id = data['user']

        db.unblocked_user(unblock_id)

        await message.answer(f"*Пользователь {unblock_id} разблокирован!* ✅️", parse_mode="Markdown")
        await bot.send_message(unblock_id, "*Вы разблокированы, по решению администратора*", parse_mode="Markdown")
        await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit(), state=Unblock.user)
async def not_Unblock(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await message.answer("Действие отменено")
    else:
        return await message.answer("ID пользователя должно состоять только из цифр, введите ID пользователя еще раз")


@dp.message_handler(lambda message: message.text.isdigit(), state=Admin.user)
async def add_user_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not db.user_exists(message.text):
            await message.answer("*Пользователь с данным ID не найден*", parse_mode="Markdown")
        else:
            data['admin'] = message.text
            admin_new = data['admin']

            db.add_admin(admin_new)

            await message.answer(f"*Вы назначили пользователя администратором:*\n\n✅ _{admin_new}_",
                                 parse_mode="Markdown")
            await bot.send_message(admin_new, "*Вас повысили до Администратора!* 😎", parse_mode="Markdown")
            await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit(), state=Admin.user)
async def not_add_user_admin(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer("_Действие отменено_", parse_mode="Markdown")
        await state.finish()
    else:
        await message.answer("_ID пользователя должно состоять только из цифр, введите ID пользователя еще раз_",
                             parse_mode="Markdown")



@dp.message_handler(lambda message: message.text.isdigit(), state=AdminDel.user)
async def del_user_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Admin"] = message.text
        admin_del = data["Admin"]

        db.del_admin(admin_del)

        await message.answer(f"*Администратор:* _{admin_del} был разжалован!_ ❌️", parse_mode="Markdown")
        await bot.send_message(admin_del, "Вас разжаловали с должности Администратора! 😔")
        await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit(), state=AdminDel.user)
async def not_del_user_admin(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer("_Действие отменено_", parse_mode="Markdown")
        await state.finish()
    else:
        await message.answer("_ID пользователя должно состоять только из цифр, введите ID пользователя еще раз_",
                             parse_mode="Markdown")
