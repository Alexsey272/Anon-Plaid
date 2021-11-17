from loader import dp, db, bot
from keyboards import *
from FSM import *
from data import config

from aiogram.types.input_media import InputMedia
from aiogram.types.input_media import InputMediaVideo
from aiogram.types.input_file import InputFile
from aiogram import Bot, types
from handlers.admins_handlers import *
from handlers.users_handlers import *

@dp.callback_query_handler(lambda call: True, state = '*')
async def process(call):
    if call.message:

        if call.data == 'confirm':
            db.add_user(call.message.chat.username, call.message.chat.id)  # добавляем юзера в табличку дб
            db.confirm(True, call.message.chat.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Ваш ответ принят ✅*",
                reply_markup=None,
                parse_mode="Markdown")
            await asyncio.sleep(1)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Для улучшеного подбора собеседника, выбери свой пол*",
                reply_markup=my_sex,
                parse_mode="Markdown")

        if call.data == 'iman':
            db.edit_sex(True, call.message.chat.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"*Регистрация завершена*",
                reply_markup=None,
                parse_mode="Markdown")

            with open('video_user/instructions.mp4', 'rb') as video:
                await bot.send_video(call.message.chat.id, video, caption = 'Ознакомьтесь с видеоинструкцией перед использованием')

        elif call.data == 'iwoman':
            db.edit_sex(False, call.message.chat.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"*Регистрация завершена*",
                reply_markup=None,
                parse_mode="Markdown")

            with open('video_user/instructions.mp4', 'rb') as video:
                await bot.send_video(call.message.chat.id, video, caption = 'Ознакомьтесь с видеоинструкцией перед использованием', reply_markup = mark_menu)

            


        if call.data == 'report':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Укажите причину жалобы_",
                reply_markup=inline_report,
                parse_mode="Markdown")

        if call.data == 'back':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Вы можете оценить своего собеседника или пожаловаться с "
                     "помощью кнопок прикрепленных к данному сообщению_",
                reply_markup=menu_like,
                parse_mode="Markdown")

        if call.data == 'spam':
            await bot.send_message(
                -1001393316058,
                f'*Поступила жалоба*\n\n*от пользователя:*\n*ID:* _'
                f'{str(call.message.chat.id)}_'
                f'\n\n*На пользователя:*\n*ID:* _'
                f'{str(db.get_last(call.message.chat.id)[0][0])}_'
                f'\n\n*Причина:* _Рассылка спама_',
                parse_mode="Markdown")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ваша жалоба отправленна на рассмотрение ✅️",
                reply_markup=None)

        if call.data == 'sale':
            await bot.send_message(
                -1001393316058,
                f'*Поступила жалоба*\n\n*от пользователя:*\n*ID:* _'
                f'{str(call.message.chat.id)}_'
                f'\n\n*На пользователя:*\n*ID:* _'
                f'{str(db.get_last(call.message.chat.id)[0][0])}_'
                f'\n\n*Причина:* _Продажа_',
                parse_mode="Markdown")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ваша жалоба отправленна на рассмотрение ✅️",
                reply_markup=None)

        if call.data == 'insult':
            await bot.send_message(
                -1001393316058,
                f'*Поступила жалоба*\n\n*от пользователя:*\n*ID:* _'
                f'{str(call.message.chat.id)}_'
                f'\n\n*На пользователя:*\n*ID:* _'
                f'{str(db.get_last(call.message.chat.id)[0][0])}_'
                f'\n\n*Причина:* _Оскорбление_',
                parse_mode="Markdown")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ваша жалоба отправленна на рассмотрение ✅️",
                reply_markup=None)

        if call.data == 'porno':
            await bot.send_message(
                -1001393316058,
                f'*Поступила жалоба*\n\n*от пользователя:*\n*ID:* _'
                f'{str(call.message.chat.id)}_'
                f'\n\n*На пользователя:*\n*ID:* _'
                f'{str(db.get_last(call.message.chat.id)[0][0])}_'
                f'\n\n*Причина:* _Распространение порнографии_',
                parse_mode="Markdown")
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Ваша жалоба отправленна на рассмотрение ✅️",
                reply_markup=None)

        if call.data == 'like':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Спасибо за вашу оценку ✅️",
                reply_markup=None)

            await bot.send_message(db.get_last(call.message.chat.id)[0][0], "Собеседник поставил вам лайк 👍")

        if call.data == 'dislike':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Спасибо за вашу оценку ✅️",
                reply_markup=None)

            await bot.send_message(db.get_last(call.message.chat.id)[0][0], "Собеседник поставил вам дизлайк 👎")

        if call.data == 'link':
            if call.message.from_user.username is not None:
                await bot.send_message(
                    db.select_connect_with_self(call.message.chat.id)[0],
                    '@' + str(db.get_name_user(call.message.chat.id)))
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="✅ *Ваша ссылка отправлена собеседнику*",
                    parse_mode="Markdown",
                    reply_markup=None)
            else:
                await bot.send_message(
                    call.message.chat.id,
                    'У вас не указан никнейм в настройках телеграма!',
                    parse_mode="Markdown")

        if call.data == 'vk':
            if db.get_vk(call.message.chat.id)[0] is None:
                await bot.send_message(
                    call.message.chat.id,
                    '*У вас не указана сыллка на вашу страницу в вк*\n\n'
                    '_Чтобы добавить ссылку на страницу в вк, воспользуйтесь '
                    'командой /account в меню бота вне диалога!_',
                    parse_mode="Markdown")
            else:
                await bot.send_message(
                    db.select_connect_with_self(call.message.chat.id)[0],
                    str(db.get_vk(call.message.chat.id)[0]))
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="✅ *Ваша ссылка отправлена собеседнику*",
                    parse_mode="Markdown",
                    reply_markup=None)

        if call.data == 'insta':
            if db.get_insta(call.message.chat.id)[0] is None:
                await bot.send_message(
                    call.message.chat.id,
                    '*У вас не указана сыллка на вашу страницу в instagram*\n\n'
                    '_Чтобы добавить ссылку на страницу в instagram, воспользуйтесь командой /account в меню бота вне диалога!_',
                    parse_mode="Markdown")
            else:
                await bot.send_message(
                    db.select_connect_with_self(call.message.chat.id)[0],
                    str(db.get_insta(call.message.chat.id)[0]))
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="✅ *Ваша ссылка отправлена собеседнику*",
                    parse_mode="Markdown",
                    reply_markup=None)

        if call.data == 'not_link':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Действие отменено_",
                reply_markup=None,
                parse_mode="Markdown")

        if call.data == 'stg_edit_sex':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='*Укажите ваш пол:*',
                reply_markup=edit_sex,
                parse_mode='Markdown')


        if call.data == 'edit_vk':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='*Отправь ссылку на свою страницу в ВКонтакте*\n\n'
                     '_Для отмены, отправьте слово "Отмена"_',
                reply_markup=None,
                parse_mode='Markdown')
            await Form.vk.set()

        if call.data == 'edit_instagram':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None,
                text='*Отправь ссылку на свой Instagram аккаунт*'
                     '\n\n_Для отмены, отправьте слово "Отмена"_',
                parse_mode='Markdown')
            await Form.insta.set()

        if call.data == 'edit_sex':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Выберите пол чтобы изменить_",
                reply_markup=edit_sex,
                parse_mode='Markdown')

        if call.data == 'edit_male':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Пол изменен на: Мужской_",
                reply_markup=None,
                parse_mode='Markdown')
            db.edit_sex(True, call.message.chat.id)

        if call.data == 'edit_female':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="_Пол изменен на: Женский_",
                reply_markup=None,
                parse_mode='Markdown')
            db.edit_sex(False, call.message.chat.id)

        if call.data == 'log':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Логи предоставлены*",
                reply_markup=None,
                parse_mode='Markdown')

            await bot.send_document(call.message.chat.id, open("all_log.log", 'rb'))

        if call.data == 'all_admin':
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Список администраторов предоставлен*",
                reply_markup=None,
                parse_mode='Markdown')
            for i in db.all_admin_exists():
                await bot.send_message(call.message.chat.id, f"Администратор: {i[0]}")

        if call.data == 'add_admin':
            if str(call.message.chat.id) == config.BOT_OWNER:
                await Admin.user.set()
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Введите ID пользователя, которого хотите назначить администратором:*\n\n_Для отмены действия, отправь слово 'Отмена'_",
                reply_markup=None,
                parse_mode='Markdown')
            else:
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ *Команда доступна только владельцу чата*",
                reply_markup=None,
                parse_mode='Markdown')

        if call.data == 'del_admin':
            if str(call.message.chat.id) == config.BOT_OWNER:
                await AdminDel.user.set()
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Введите ID администратора, которого хотите разжаловать:*\n\n_Для отмены действия, отправь слово 'Отмена'_",
                reply_markup=None,
                parse_mode='Markdown')
            else:
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ *Команда доступна только владельцу чата*",
                reply_markup=None,
                parse_mode='Markdown')

        if call.data == 'ban':
            if db.admin_exists(call.message.chat.id):
                await Block.user.set()
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Отправьте ID пользователя, которого хотите заблокировать*"
            "\n\n_Для отмены действия, отправьте слово 'Отмена'_",
                reply_markup=None,
                parse_mode='Markdown')
            else:
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ *Команда доступна только администраторам*",
                reply_markup=None,
                parse_mode='Markdown')

        if call.data == 'unban':
            if db.admin_exists(call.message.chat.id):
                await Unblock.user.set()
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="*Введите ID пользователя, которого хотите разблокировать*\n\n_Для отмены действия, отправьте слово 'Отмена'_",
                reply_markup=None,
                parse_mode='Markdown')
            else:
                await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ *Команда доступна только администраторам*",
                reply_markup=None,
                parse_mode='Markdown')

        await call.answer()