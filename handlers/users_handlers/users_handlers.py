from loader import dp, db, bot, now
import asyncio
from aiogram import Bot, types
from keyboards import *
from FSM import *
from aiogram.types.message import ContentTypes
import aiogram.utils.exceptions
import datetime
from datetime import *
from aiogram.utils.exceptions import Throttled
import requests
from data import config
from utils.logging import warning_log

# хендлер команды /start
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):

    if not db.user_exists(message.from_user.id):
        await Register.confirm.set()
        await message.answer(
            'Вы соглашаетесь с [правилами](https://telegra.ph/Pravila-anonimnogo-chata-Crimson-Plaid-07-12) общения в Анонимном чате',
            reply_markup=confirm_button, parse_mode="Markdown")
    else:
        sex = db.get_sex_user(message.from_user.id)

        await state.finish()

        if sex[0] is None:

            await message.answer("Для улучшеного подбора собеседника, выбери свой пол", reply_markup=my_sex)
        else:

            if not db.subscribtion_exists(message.from_user.id):
                await bot.send_message(message.chat.id,
                                       f"*CRIMSON PLAID*\n\n*Наше сообщество ВКонтакте:*"
                                       f"\n_Подпишись - https://vk.com/crimsonplaid_\n\n_Для управления ботом, "
                                       f"воспользуйтесь клавиатурой появившейся в нижней части_ 😉",
                                       reply_markup=mark_menu, parse_mode="Markdown")


            elif db.subscribtion_exists(message.from_user.id):

                from_by = datetime.strptime(db.by_subscribtion(message.from_user.id)[0][2], '%Y-%m-%d')

                if from_by < now:
                    db.del_subscribtion(message.from_user.id)
                    await bot.send_message(message.chat.id,
                                           f"*CRIMSON PLAID*\n\n*Наше сообщество ВКонтакте:*\n"
                                           f"_Подпишись - https://vk.com/crimsonplaid_\n\n"
                                           f"_Для управления ботом, воспользуйтесь клавиатурой "
                                           f"появившейся в нижней части_ 😉",
                                           reply_markup=mark_menu, parse_mode="Markdown")
                else:
                    await bot.send_message(message.chat.id,
                                           f"*CRIMSON PLAID*\n\n_Для управления ботом, воспользуйтесь клавиатурой "
                                           f"появившейся в нижней части_ 😉",
                                           reply_markup=mark_menu, parse_mode="Markdown")


@dp.message_handler(content_types=ContentTypes.TEXT, state=Register.confirm)
async def confirm_true(message: types.Message, state: FSMContext):

    if message.text == 'С правилами ознакомлен ✅️':

        db.add_user(message.from_user.username, message.from_user.id)  # добавляем юзера в табличку дб
        db.confirm(True, message.from_user.id)
        await message.answer("Ваш ответ принят!")
        await Register.next()
        await message.answer("Укажите ваш пол:", reply_markup = my_sex)
    else:
        await message.answer("Для начала, вам нужно ознакомиться с правилами, и согласится с ними чтобы продолжить")

@dp.message_handler(content_types=ContentTypes.TEXT, state=Register.sex)
async def sex_select(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['info'] = message.text


        if data['info'] == "Парень 👨":
            await state.finish()
            db.edit_sex(True, message.from_user.id)
            await message.answer("*Указан пол:* мужской", parse_mode = "Markdown")
            with open('files/video_user/instructions.mp4', 'rb') as video:
                await bot.send_video(message.chat.id, video, caption="Рекомендуем, ознакомится с короткой видеоинструкцией, об использовании бота")
            await start(message, state)

        elif data['info'] == "Девушка 👩":
            await state.finish()
            db.edit_sex(False, message.from_user.id)
            await message.answer("*Указан пол:* Женский", parse_mode = "Markdown")
            with open('files/video_user/instructions.mp4', 'rb') as video:
                await bot.send_video(message.chat.id, video, caption="Рекомендуем, ознакомится с короткой видеоинструкцией, об использовании бота")
            await start(message, state)
        

        else:
            await message.answer("Укажите ваш пол, чтобы продолжить, он понадобится для поиска по полу")


@dp.message_handler(lambda message: message.text == 'Начать поиск 🔍', state='*')
async def search(message: types.Message):
    sub_channel = await bot.get_chat_member(-1001576490683, message.from_user.id)

    if sub_channel.status == "left":
        await message.answer(
            '❌️ *Бот доступен только для подписчиков канала*\n\n'
            '_Подпишитесь на канал, перейдя по ссылке, чтобы продолжить_',
            reply_markup=channel_menu, parse_mode = " Markdown")
    else:
        await message.answer('*🔎 Выберите один из режимов поиска:*', reply_markup=search_menu, parse_mode = "Markdown")


@dp.message_handler(lambda message: message.text == 'Поиск по полу 👫', state='*')
async def sex_search(message: types.Message):
    await message.answer('*Выберите пол собеседника: *', reply_markup=sex_menu, parse_mode = "Markdown")


@dp.message_handler(commands=['commands'])
async def commands(message: types.Message):
    await message.answer(
        '*Список команд чата*\n_Команды для использования в чате, при общении с собеседником_\n\n'
        '*/kiss* - _Поцеловать собеседника_\n\n*/hud* - _Обнять собеседника_\n\n*/pat* - _Погладить собеседника_'
        '\n\n*/wink* - _Подмигнуть собеседнику_\n\n*/slap* - _Отшлепать собеседника_\n\n*/bite* - _Сделать кусь собеседнику_',
        parse_mode='Markdown')


@dp.message_handler(commands=['terms'])
async def support(message: types.Message):
    await message.answer(
        '[Правила](https://telegra.ph/Pravila-anonimnogo-chata-Crimson-Plaid-07-12) поведения в Анонимном чате, советуем ознакомится перед использованием',
        parse_mode="Markdown")

@dp.message_handler(commands=['help'])
async def support(message: types.Message):
    await message.answer('Краткая [Инструкция](https://telegra.ph/Instrukciya-Anonimnogo-chata-08-12) по использованию анонимного чата.\n\nЕсли еще остались вопросы, вы можете их задать в нашем чате Тех поддержки - @CrimsonChatSupport \n\nЕсли возник серьезный вопрос в плане работы чата, используйте команду /support, чтобы отправить письмо в службу поддержки.\n\nПо вопросам рекламы обращайтесь к администратору @kseniafilatova228',
        parse_mode="Markdown")


@dp.message_handler(commands=['account'])
@dp.message_handler(lambda message: message.text == 'Мой аккаунт 👤')
async def price(message: types.Message):
    account = db.get_account(message.from_user.id)[0]

    if str(db.get_media(message.from_user.id)[0]).endswith("mp4"):
        with open('files/video_user/avatars/' + str(message.from_user.id) + '.mp4', 'rb') as video:
            await bot.send_video(message.chat.id, video,
                                 caption=f"{account[10]}, {account[9]}\n\n*Instagram:* "
                                         f"{account[8]}\n*Вконтакте:* {account[7]}",
                                 parse_mode="Markdown")

    elif str(db.get_media(message.from_user.id)[0]).endswith("jpg"):
        with open('files/photo_user/avatars/' + str(message.from_user.id) + '.jpg', 'rb') as photoid:
            await bot.send_photo(message.chat.id, photoid,
                                 caption=f"{account[10]}, {account[9]}\n\n*Instagram:* "
                                         f"{account[8]}\n*Вконтакте:* {account[7]}",
                                 parse_mode="Markdown")

    else:
        await message.answer(
            f"*Nikname:* _{account[10]}_\n*Город:* _{account[9]}_\n"
            f"*Instagram:* _{account[8]}_\n*Вконтакте:* _{account[7]}_", parse_mode = "Markdown")

    await message.answer("1. Изменить никнейм\n2. Изменить фото\n3. Изменить текст анкеты\n4. изменить ссылку Instagram\Вконтакте\n5.Изменить город", reply_markup = select_menu)
    await Account.select.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Account.select)
async def not_add_photo_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "1":
            await state.finish()
            await bot.send_message(
                message.chat.id,
                '*Как мне вас называть?*'
                     '\n\n_Никнейм должен состоять не больше чем из 30 символов и не меньше 5 символов_'
                     '\n\n_Для отмены, отправьте слово "Отмена"_',
                reply_markup = None,
                parse_mode='Markdown')
            await Form.nickname.set()
        
        elif message.text == "2":
            await state.finish()
            await bot.send_message(
                message.chat.id,
                '*Отправь фото, которое ты хочешь поставить на аватарку*\n\n_для отмены отправь слово "Отмена"_',
                reply_markup=None,
                parse_mode='Markdown'
            )
            await Form.photo.set()

        elif message.text == "3":
            await message.answer("Функция временно недоступна")

        elif message.text == "4":
            await bot.send_message(
                    message.chat.id,
                    "_Выберить соц сеть, ссылку к которой вы хотите добавить или изменить_",
                    reply_markup=menu_social,
                    parse_mode='Markdown')
            await state.finish()
        elif message.text == "5":
            await state.finish()
            await bot.send_message(
                message.chat.id,
                '*Отправь вашу геолокацию чтобы добавить город*'
                     '\n\n_Для отмены, отправьте слово "Отмена"_',
                reply_markup = None,
                parse_mode='Markdown')
            await Form.city.set()

        elif message.text == "Назад 🔙":
            await state.finish()
            await start(message, state)

@dp.message_handler(commands=['settings'])
async def settings(message: types.Message):
    await message.answer(
        "*Настройки*\n\n_Выберите пункт для настройки_",
        parse_mode="Markdown", reply_markup = settings_menu)

@dp.message_handler(lambda message: db.blocked_exists(message.from_user.id) == True)
async def block(message: types.Message):
    await message.answer(
        "*Вы заблокированы!* ⛔️\n\n_Вы можете оспорить блокировку, написав в службу поддержки. Для этого отправьте команду /support_",
        parse_mode="Markdown")


@dp.message_handler(commands=['support'])
async def send_report(message: types.Message):
    await Report.info.set()
    await message.answer(
        '_Опишите вашу проблему в подробностях,и мы постараемся ее решить в ближайшее время, и ответить на все вопросы'
        '\n\n_Для отправкий заявки в тех поддержку, отправьте текст сообщения с подробным описание вопроса или '
        'отправьте фото с прикрепленным текстом, чтобы к заявке прикрепить фото_\n\n'
        'Для отмены, отправьте слово "Отмена"_',
        parse_mode="Markdown")


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.answer('@Crimson\_plaid\_bot - Анонимный чат для знакомств и анонимного общения\n\nНаша основная группа в [VKontakte](https://vk.com/crimsonplaid), здесь публикуется вся информация касаемо Анонимного чата.\n\n@CrimsonNews -  канал где публикуются новости и обновления.\n\nНаша группа в [Twitter](https://twitter.com/crimson_plaid) где так же вы найдете информацию о новых версиях и нововведениях\n\nРепозиторий нашего чата на [Github](https://github.com/Alexsey272/Anon-Plaid)\n\n*Версия:* _ОБТ v0.3_',parse_mode="Markdown")

@dp.message_handler(content_types=ContentTypes.PHOTO, state=Report.info)
async def add_photo_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.caption
        info = data['info']

        await message.photo[-1].download('files/photo_user/' + str(message.from_user.id) + 'report.jpg')
        with open('files/photo_user/' + str(message.from_user.id) + 'report.jpg', 'rb') as photo:
            await bot.send_photo(config.BOT_OWNER, photo,
                                 caption=f"*Сообщение от пользователя:*\n_{message.from_user.id}_\n\n_{info}_",
                                 parse_mode="Markdown")
        await message.answer(
            "✅ _Ваше сообщение отправленно Администратору на рассмотрение, после рассмотрения, вам ответят_",
            parse_mode="Markdown")

        await state.finish()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Report.info)
async def not_add_photo_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if message.text.lower() == "отмена":
            await state.finish()
            await message.answer("_Действие отменено_", parse_mode="Markdown")
            await start(message, state)
        else:
            data['info'] = message.text
            info = data['info']
            await bot.send_message(config.BOT_OWNER, f"*Сообщение от пользователя:*\n_{message.from_user.id}\n\n{info}_",
                                   parse_mode="Markdown")
            await message.answer(
                "✅ _Ваше сообщение отправлено Администратору на рассмотрение, после рассмотрениея, вам ответят_",
                parse_mode="Markdown")
            await state.finish()


@dp.message_handler(content_types=ContentTypes.LOCATION, state=Form.city)
async def add_city(message: types.Message, state: FSMContext):
    longitude = message.location.longitude
    latitude = message.location.latitude

    r = requests.get(
        f'https://geocode-maps.yandex.ru/1.x?format=json&lang=ru_RU&kind=house&geocode={longitude},{latitude}&'
        f'apikey={config.YANDEX_API}')
    json_data = r.json()

    address = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["AddressDetails"]["Country"]['AdministrativeArea']['SubAdministrativeArea']['Locality'][
        'LocalityName']

    await state.finish()
    db.add_city(message.from_user.id, address)
    await message.answer(f"*Установлен город:* _{address}_", parse_mode="Markdown")
    await start(message, state)


@dp.message_handler(state=Form.city)
async def add_city(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await message.answer('Действие отменено')
        await start(message, state)
    else:
        return await message.answer('*Я вас не понимаю, отправьте пожалуйста вашу геолокацию, '
                                    'или отправьте слово "Отмена", чтобы отменить действие*', parse_mode="Markdown")


@dp.message_handler(state=Form.nickname)
async def add_nickname(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.finish()
        await message.answer('Действие отменено')
        await start(message, state)
    else:
        if len(message.text) > 30 or len(message.text) < 5:
            await message.answer(
                '*Никнейм не должен состоять больше чем из 30 символов или меньше 5 символов*',
                parse_mode="Markdown")
        else:
            try:
                async with state.proxy() as data:
                    data['nickname'] = message.text
                    await state.finish()
                    db.add_nickname(message.from_user.id, data['nickname'])
                    await message.answer(f"*Ваш никнейм:* _{data['nickname']}_", parse_mode="Markdown")
                    await start(message, state)

            except sqlite3.IntegrityError:
                await message.answer(
                    f"*Никнейм:* _{data['nickname']}_"
                    f"\n\n_Уже существует, попробуйте что то другое_", parse_mode="Markdown")
                await Form.nickname.set()


@dp.message_handler(state=Form.vk)
async def add_vk(message: types.Message, state: FSMContext):
    try:
        entity = message.entities[0]

        if entity.type in ["url"]:
            if "vk.com" in message.text:
                async with state.proxy() as data:
                    data['vk'] = message.text
                    await state.finish()
                    db.add_vk(message.from_user.id, data['vk'])
                    await message.answer(f"*Ваша ссылка в вк: * _{data['vk']}_", parse_mode="Markdown")
                    await start(message, state)
            else:
                await message.answer('⚠️ *Ссылка не является, ссылкой на аккаунт вк, отправьте ссылку на страницу вк*',
                                     parse_mode="Markdown")
        else:
            await message.answer("⚠️ *Отправьте пожалуйста ссылку на ваш аккаунт ВКонтакте*", parse_mode="Markdown")

    except IndexError:
        if message.text.lower() == "отмена":
            await state.finish()
            await message.answer("Действие отменено")
            await start(message, state)
        else:
            await message.answer("⚠️ *Отправьте пожалуйста ссылку на ваш аккаунт ВКонтакте*", parse_mode="Markdown")


@dp.message_handler(state=Form.insta)
async def add_insta(message: types.Message, state: FSMContext):
    try:
        entity = message.entities[0]

        if entity.type in ["url"]:
            if "instagram.com" in message.text:
                async with state.proxy() as data:
                    data['insta'] = message.text
                    await state.finish()
                    db.add_insta(message.from_user.id, data['insta'])
                    await message.answer(f"*Ваша ссылка на Инстаграм:* _{data['insta']}_", parse_mode="Markdown")
                    await start(message, state)
            else:
                await message.answer(
                    "⚠️ *Ссылка не является, ссылкой на Instagram аккаунт, отправьте ссылку на аккаунт Instagram*",
                    parse_mode="Markdown")

        else:
            await message.answer("⚠️ *Отправьте пожалуйста ссылку на ваш Instagram аккаунт*", parse_mode="Markdown")

    except IndexError:
        if message.text.lower() == "отмена":
            await state.finish()
            await message.answer('Действие отменено')
            await start(message, state)
        else:
            await message.answer("⚠️ *Отправьте пожалуйста ссылку на ваш Instagram аккаунт*", parse_mode="Markdown")


@dp.message_handler(content_types=ContentTypes.PHOTO, state=Form.photo)
async def add_avatar(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo
        await data['photo'][-1].download('files/photo_user/avatars/' + str(message.from_user.id) + '.jpg')
        db.add_media(message.from_user.id, 'files/photo_user/avatars/' + str(message.from_user.id) + '.jpg')
        await message.answer("✅️ Фото установлено!")
        await state.finish()
        await start(message, state)


@dp.message_handler(content_types=ContentTypes.VIDEO, state=Form.photo)
async def add_avatar(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.video.file_id
        file = await bot.get_file(data['video'])
        file_path = file.file_path
        await bot.download_file(file_path, 'files/video_user/avatars/' + str(message.from_user.id) + '.mp4')
        db.add_media(message.from_user.id, 'files/video_user/avatars/' + str(message.from_user.id) + '.mp4')
        await message.answer("✅️ Видео установлено!")
        await state.finish()
        await start(message, state)


@dp.message_handler(content_types=ContentTypes.TEXT, state=Form.photo)
async def add_avatar(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer("*Действие отменено!*", parse_mode="Markdown")
        await state.finish()
        await start(message, state)
    else:
        await message.answer(
            "*Я вас не понимаю, отправьте пожалуйста фото или видео, "
            "если хотите отменить действие, отправьте слово 'Отмена'*",
            parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == 'Парня 👨' or message.text == 'Девушку 👩', state='*')
async def chooce_sex(message: types.Message, state: FSMContext):
    await state.update_data(msg=message.text)

    user_data = await state.get_data()

    try:
        if db.queue_exists(message.from_user.id):
            db.delete_from_queue(message.from_user.id)
        if user_data['msg'] == 'Парня 👨':
            db.add_to_queue(message.from_user.id, True)
            await message.answer(
                '⏳️ *Поиск собеседника,\nпожалуйста подождите...*\n\n_Мы сообщим когда найдем вам собседеника_',
                parse_mode="Markdown")
        elif user_data['msg'] == 'Девушку 👩':
            db.add_to_queue(message.from_user.id, False)
            await message.answer(
                '⏳️ *Поиск собеседника,\nпожалуйста подождите...*\n\n_Мы сообщим когда найдем вам собседеника_',
                parse_mode="Markdown")

        while True:
            await asyncio.sleep(0.5)
            if db.search(db.get_sex_user(message.from_user.id)[0]) is not None and \
                    db.search(db.get_sex_user(message.from_user.id)[0])[
                        0] != message.from_user.id:  # если был найден подходящий юзер в очереди
                try:
                    db.update_connect_with(db.search(db.get_sex_user(message.from_user.id)[0])[0],
                                           message.from_user.id)  # обновляем с кем общается юзер
                    db.update_connect_with(message.from_user.id, db.search(db.get_sex_user(message.from_user.id)[0])[0])
                    break
                except Exception as e:
                    print(e)

        if db.select_connect_with(message.from_user.id)[0] is not None:  # если пользователь законектился

            try:
                db.delete_from_queue(message.from_user.id)  # удаляем из очереди
                db.delete_from_queue(db.select_connect_with(message.from_user.id)[0])
            except:
                pass

            await Chating.msg.set()

            db.last_update(db.select_connect_with(message.from_user.id)[0], message.from_user.id)
            db.last_update(message.from_user.id, db.select_connect_with(message.from_user.id)[0])

            await bot.send_message(db.select_connect_with(message.from_user.id)[0],
                                   '🤖 *Собеседник найден!*\n_Чтобы закончить, или начать новый диалог,'
                                   'вы можете воспользоваться командами:_\n\n*/stop* _- Остановить диалог_'
                                   '\n\n_Приятного общения!_',
                                   reply_markup=menu_msg, parse_mode="Markdown")
            await bot.send_message(message.from_user.id,
                                   '🤖 *Собеседник найден!*\n_Чтобы закончить, или начать новый диалог,'
                                   'вы можете воспользоваться командами:_\n\n*/stop* _- Остановить диалог_'
                                   '\n\n_Приятного общения!_',
                                   reply_markup=menu_msg, parse_mode="Markdown")

    except Exception as e:
    	if "bot was blocked" in str(e):
    		await message.answer("Собеседник заблокировал бота, попробуйте снова")
    		db.delete_block_user(db.select_connect_with(message.from_user.id)[0], message.from_user.id, None)
    		await start(message, state)
    	warning_log.warning(e)
    	await send_to_channel_log_exception(message, e)

@dp.message_handler(commands = ['search'], state='*')
@dp.message_handler(lambda message: message.text == 'Рандомный поиск 🔎', state='*')
async def random_search(message: types.Message, state: FSMContext):
    try:
        if db.queue_random_exists(message.from_user.id):
            db.delete_from_random_queue(message.from_user.id)

        db.add_to_random_queue(message.from_user.id, bool(db.get_sex_user(message.from_user.id)))
        await message.answer(
            '⏳️ *Поиск собеседника,\nпожалуйста подождите...*\n\n_Мы сообщим когда найдем вам собседеника_ ',
            parse_mode="Markdown")

        while True:
            await asyncio.sleep(0.5)
            if db.search_random() is not None and db.search_random()[
                0] != message.from_user.id:  # если был найден подходящий юзер в очереди
                try:

                    db.update_connect_with(db.search_random()[0], message.from_user.id)  # обновляем с кем общается юзер
                    db.update_connect_with(message.from_user.id, db.search_random()[0])
                    break
                except Exception as e:
                    print(e)

        if db.select_connect_with(message.from_user.id)[0] is not None:  # если пользователь законектился

            try:
                db.delete_from_random_queue(message.from_user.id)  # удаляем из очереди
                db.delete_from_random_queue(db.select_connect_with(message.from_user.id)[0])
            except:
                pass

            db.last_update(db.select_connect_with(message.from_user.id)[0], message.from_user.id)
            db.last_update(message.from_user.id, db.select_connect_with(message.from_user.id)[0])

            if db.get_sex_user(message.from_user.id)[0] == 1:
                a = '🧑 Парень'
            else:
                a = '👧 Девушка'

            if db.get_sex_user(db.select_connect_with(message.from_user.id)[0]) == 1:
                b = '🧑 Парень'

            else:
                b = '👧 Девушка'

            await Chating.msg.set()

            await bot.send_message(db.select_connect_with(message.from_user.id)[0],
                                   '🤖 *Собеседник найден!*\n\nПол: ' + a + '\n\n_Чтобы закончить, или начать новый диалог, '
                                   'вы можете воспользоваться командами:_\n\n*/stop* _- Остановить диалог_'
                                   '\n\n_Приятного общения!_',
                                   reply_markup=menu_msg, parse_mode="Markdown")
            await bot.send_message(message.from_user.id,
                                   '🤖 *Собеседник найден!*\n\nПол: ' + b + '\n\n_Чтобы закончить, или начать новый диалог, '
                                   'вы можете воспользоваться командами:_\n\n*/stop* _- Остановить диалог_'
                                   '\n\n_Приятного общения!_',
                                   reply_markup=menu_msg, parse_mode="Markdown")


    except Exception as e:
    	if "bot was blocked" in str(e):
    		await message.answer("Собеседник заблокировал бота, попробуйте снова")
    		db.delete_block_user(db.select_connect_with(message.from_user.id)[0], message.from_user.id, None)
    		await start(message, state)
    	warning_log.warning(e)
    	await send_to_channel_log_exception(message, e)

@dp.message_handler(commands=['kiss'], state = Chating.msg)
async def kiss(message: types.Message):
    await message.answer(
        '*Вы поцеловали собеседника*',
        parse_mode="Markdown")
    await bot.send_video(
            db.select_connect_with(message.from_user.id)[0],
            'https://tenor.com/bk57O.gif',
            caption='*Собеседник вас поцеловал*',
            parse_mode='Markdown')

@dp.message_handler(commands=['hud'], state = Chating.msg)
async def hud(message: types.Message):
    await message.answer(
        '*Вы обняли собеседника*',
        parse_mode='Markdown')
    await bot.send_video(
                db.select_connect_with(message.from_user.id)[0],
                'https://tenor.com/bb9kg.gif',
                caption='*Собеседник обнял вас*',
                parse_mode='Markdown')

@dp.message_handler(commands=['pat'], state = Chating.msg)
async def pat(message: types.Message):
    await message.answer(
        '*Вы погладили собеседника*',
        parse_mode='Markdown')
    await bot.send_video(
                db.select_connect_with(message.from_user.id)[0],
                'https://tenor.com/AkZm.gif',
                caption='*Собеседник погладил вас*',
                parse_mode='Markdown')

@dp.message_handler(commands=['wink'], state = Chating.msg)
async def wink(message: types.Message):
    await message.answer(
        '*Вы подмигнули собеседнику*',
        parse_mode='Markdown')
    await bot.send_video(
                db.select_connect_with(message.from_user.id)[0],
                'https://tenor.com/Ny7S.gif',
                caption='*Собеседник вам подмигнул*',
                parse_mode='Markdown')

@dp.message_handler(commands=['slap'], state = Chating.msg)
async def slap(message: types.Message):
    await message.answer(
        '*Вы отшлепали собеседника*',
        parse_mode='Markdown')
    await bot.send_video(
                db.select_connect_with(message.from_user.id)[0],
                'https://tenor.com/7EU6.gif',
                caption='*Собеседник вас отшлепал*',
                parse_mode='Markdown')


@dp.message_handler(commands=['bite'], state = Chating.msg)
async def bite(message: types.Message):
    await message.answer(
        '*Вы сделали кусь собеседнику*',
        parse_mode='Markdown')
    await bot.send_video(
                db.select_connect_with(message.from_user.id)[0],
                'https://tenor.com/Z8Tf.gif',
                caption='*Собеседник вам сделал кусь*',
                parse_mode='Markdown')

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди :)")

@dp.message_handler(content_types=ContentTypes.TEXT)
@dp.message_handler(state=Chating.msg)
@dp.throttled(anti_flood,rate=1)
async def chat(message: types.Message, state: FSMContext):
    try:
        await state.update_data(msg=message.text)

        user_data = await state.get_data()

        if user_data['msg'] == '✉️ Отправить ссылку на себя':
            await message.answer(
                '⚠️ *Вы действительно хотите отправить ссылку на одну из своих строниц?'
                'Действие нельзя будет отменить, в случаи согласия, собеседник получит ссылку на вашу'
                'страницу в социальной сети*',
                parse_mode="Markdown",
                reply_markup=link_menu)

        elif user_data['msg'] == '❌Остановить диалог' or user_data['msg'] == '/stop':
            if db.select_connect_with(message.from_user.id)[0] is not None:
                await state.finish()
                await message.answer(
                    '*Диалог закончен*\n\n_Чтобы начать новый диалог, используйте команду /search_',
                    reply_markup=mark_menu,
                    parse_mode='Markdown')
                await message.answer(
                    '_Вы можете оценить своего собеседника или пожаловаться с '
                    'помощью кнопок прикрепленных к данному сообщению_',
                    reply_markup=menu_like,
                    parse_mode='Markdown')
                await bot.send_message(
                    db.select_connect_with(message.from_user.id)[0],
                    '*Диалог закончен*\n\n_Чтобы начать новый диалог, используйте команду /search_',
                    reply_markup=mark_menu,
                    parse_mode='Markdown')
                await bot.send_message(
                    db.select_connect_with(message.from_user.id)[0],
                    '_Вы можете оценить своего собеседника с помощью кнопок прикрепленных к данному сообщению_',
                    reply_markup=menu_like,
                    parse_mode='Markdown')
                db.update_connect_with(None, db.select_connect_with(message.from_user.id)[0])
                db.update_connect_with(None, message.from_user.id)
            else:
                await message.answer("Вы не состоите в диалоге")


        elif user_data['msg'] == 'Назад 🔙':
            await start(message, state)
            await state.finish()

        else:

            try:
                entity = message.entities[0]
                if entity.type in ["url", "text_link"]:
                    await message.answer('Отправка ссылок запрещена!')
                    await bot.send_message(
                        db.select_connect_with(message.from_user.id)[0],
                        "Ссылка удалена!")

            except (AttributeError, IndexError):
                await bot.send_message(db.select_connect_with(message.from_user.id)[0],
                                       user_data['msg'])  # отправляем сообщения пользователя
                db.log_msg(message.from_user.id, user_data['msg'])  # отправка сообщений юзеров в бд
                await send_to_channel_log(message)



    except aiogram.utils.exceptions.ChatIdIsEmpty:
        await state.finish()
        if db.queue_random_exists(message.from_user.id) or db.queue_exists(message.from_user.id):
            await bot.send_message(message.chat.id,
                                   "_Вы еще не состоите в диалоге, подождите "
                                   "пожалуйста, скоро мы найдем вам собеседника_",
                                   parse_mode="Markdown")
        else:
            await start(message, state)
    except aiogram.utils.exceptions.BotBlocked:
    	await message.answer("😔 Собеседник заблокировал бота!")
    	db.delete_block_user(db.select_connect_with(message.from_user.id)[0], message.from_user.id, None)
    	await state.finish()
    	await start(message, state)
    except Exception as e:
    	warning_log.warning(e)
    	await send_to_channel_log_exception(message, e)


@dp.message_handler(content_types=ContentTypes.PHOTO,state='*')
async def chating_photo(message: types.Message, state: FSMContext):

    if db.select_connect_with(message.from_user.id)[0] != None:
        try:
            await message.photo[-1].download('files/photo_user/' + str(message.from_user.id) + '.jpg')

            with open('files/photo_user/' + str(message.from_user.id) + '.jpg', 'rb') as photoid:
                await bot.send_photo(db.select_connect_with(message.from_user.id)[0], photoid, caption=message.caption)
        
        except Exception as e:
            warning_log.warning(e)
            await send_to_channel_log_exception(message, e)


@dp.message_handler(content_types=ContentTypes.VIDEO, state='*')
async def chating_video(message: types.Message, state: FSMContext):

    if db.select_connect_with(message.from_user.id)[0] != None:
        try:
            file_id = message.video.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, 'files/video_user/' + str(message.from_user.id) + '.mp4')
            with open('files/video_user/' + str(message.from_user.id) + '.mp4', 'rb') as video:
                await bot.send_video(db.select_connect_with(message.from_user.id)[0], video, caption=message.text)
        except Exception as e:
            warning_log.warning(e)
            await send_to_channel_log_exception(message, e)


@dp.message_handler(content_types=ContentTypes.CONTACT, state='*')
async def chating_contact(message: types.Message, state: FSMContext):
    if db.select_connect_with(message.from_user.id)[0] != None:
        phone = message.contact.phone_number
        name = message.contact.first_name
        last_name = message.contact.last_name
        await bot.send_contact(db.select_connect_with(message.from_user.id)[0], phone, name, last_name)


@dp.message_handler(content_types=ContentTypes.VOICE, state='*')
async def chating_voice(message: types.Message, state: FSMContext):
    if db.select_connect_with(message.from_user.id)[0] != None:
        try:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, 'files/voice_user/' + str(message.from_user.id) + '.ogg')
            with open('files/voice_user/' + str(message.from_user.id) + '.ogg', 'rb') as voice:
                await bot.send_voice(db.select_connect_with(message.from_user.id)[0], voice, caption=message.text)
    
        except Exception as e:
            warning_log.warning(e)
            await send_to_channel_log_exception(message, e)


@dp.message_handler(content_types=ContentTypes.AUDIO, state='*')
async def audio(message: types.Message, state: FSMContext):
    if db.select_connect_with(message.from_user.id)[0] != None:
        try:
            file_id = message.audio.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, 'files/audio_user/' + str(message.from_user.id) + '.mp3')
            with open('files/audio_user/' + str(message.from_user.id) + '.mp3', 'rb') as audioid:
                await bot.send_audio(db.select_connect_with(message.from_user.id)[0], audioid, caption=message.text)
        except Exception as e:
            warning_log.warning(e)
            await send_to_channel_log_exception(message, e)


@dp.message_handler(content_types=ContentTypes.STICKER,state='*')
async def chating_sticker(message: types.Message, state: FSMContext):
    if db.select_connect_with(message.from_user.id)[0] != None:
        try:
            await bot.send_sticker(db.select_connect_with(message.from_user.id)[0], message.sticker.file_id)
        except Exception as e:
            warning_log.warning(e)
            await send_to_channel_log_exception(message, e)

# логи в телеграм канал
async def send_to_channel_log(message: types.Message):
    await bot.send_message(config.DIALOG,
                           f'ID - {str(message.from_user.id)}\n'
                           f'username - @{str(message.from_user.username)}\n'
                           f'message - {str(message.text)}')


async def send_to_channel_log_exception(message: types.Message, except_name):
    await bot.send_message(config.ERROR, f'Ошибка\n\n{except_name}')

# хендлер для команды назад
@dp.message_handler(commands=['back'])
@dp.message_handler(lambda message: message.text == 'Назад 🔙', state='*')
async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await start(message, state)