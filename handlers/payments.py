from yoomoney import Quickpay,Client
from loader import dp,bot,db,now
from aiogram import types
from keyboards import *
from datetime import *
from aiogram.types.message import ContentType
from FSM import *
import random
from data import config

@dp.message_handler(commands=['pay'])
@dp.message_handler(lambda message: message.text == 'Подписка 💲', state='*')
async def price(message: types.Message):
    if not db.subscribtion_exists(message.from_user.id):
        await bot.send_message(message.chat.id,
                               "*Премиум-подписка*\n\nНаш чат имеет только бесплатный функционал, но премиум подписка позволяет избавится "
                               "от рекламы, а так же приобретая подписку, вы поддерживаете наш проект\n\n"
                               "Преимущество премиум подписок:\n\n✅️ *Отключение рекламы*\n"
                               "Премиум подписчики не будут видеть рекламу в нашем чате\n\n"
                               "✅️ *Поддержка проекта*\nПоддерживая наш проект, вы мотивируете нас на улучшения"
                               " чата, а так же поддерживаете его работу",
                               reply_markup=subscription_menu, parse_mode="Markdown")
        await message.answer('*Выберите длительность подписки и удобный способ оплаты:*', parse_mode = "Markdown")


    elif db.subscribtion_exists(message.from_user.id):

        type_sub = db.by_subscribtion(message.from_user.id)[0][4]
        from_by = datetime.strptime(db.by_subscribtion(message.from_user.id)[0][2], '%Y-%m-%d')

        if from_by < now:
            db.del_subscribtion(message.from_user.id)
            await bot.send_message(message.chat.id,
                                   "*Премиум-подписка*\n\nНаш чат имеет только бесплатный функционал, но премиум подписка позволяет "
                                   "избавится от рекламы, а так же приобретая подписку, вы поддерживаете наш проект"
                                   "\n\nПреимущество премиум подписок:\n\n✅️ *Отключение рекламы*"
                                   "\nПремиум подписчики не будут видеть рекламу в нашем чате\n\n"
                                   "✅️ *Поддержка проекта*\nПоддерживая наш проект, вы мотивируете нас на улучшения"
                                   " чата, а так же поддерживаете его работу",
                                   reply_markup=subscription_menu, parse_mode="Markdown")
            await message.answer('*Выберите длительность подписки, и удобный способ оплаты:*', parse_mode = "Markdown")

        elif from_by >= now:
            await message.answer(
                "*У вас уже оформлена подписка {0}*\n\n_Подписка действительна до {1}_"
                "\n\n_Возвращайтесь попозже 😉_".format(
                    type_sub, from_by), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == '79₽ за 7 дней' or
                                    message.text == '130₽ за 30 дней' or
                                    message.text == '599₽ за 365 дней', state='*')
async def buy_st(message: types.Message):
    global title, about, photo, price_sub

    if message.text == '79₽ за 7 дней':
        title = "Подписка Standard"
        about = "Подписка стандарт, на 7 дней, полный пакет возможностей"
        photo = "https://i.ibb.co/5sM0S8d/standart.png"
        price_sub = 79
        num="ST"

    if message.text == '130₽ за 30 дней':
        title = "Подписка Premium"
        about = "Подписка премиум, на 1 месяц, полный пакет возможностей"
        photo = "https://i.ibb.co/Lv0FVdR/premium.png"
        price_sub = 139
        num="PR"

    if message.text == '599₽ за 365 дней':
        title = "Подписка VIP"
        about = "Подписка ВИП, на 1 год, полный пакет возможностей"
        photo = "https://i.ibb.co/7SL38yq/vip.png"
        price_sub = 599
        num="VP"

    quickpay = Quickpay(
            receiver="410012801752426",
            quickpay_form="shop",
            targets=title,
            formcomment=about,
            short_dest=about,
            paymentType="SB",
            sum=price_sub,
            label=f"{num}{message.from_user.id}"
            )


    payments = InlineKeyboardButton("Заплатить", url  = str(quickpay.redirected_url))
    pay_menu = InlineKeyboardMarkup().add(payments)

    await bot.send_photo(message.chat.id, photo, caption=f"*{title}*\n\n{about}\n\n*Стоимость: *{str(price_sub)}RUB",parse_mode = "Markdown", reply_markup = pay_menu)

@dp.message_handler(commands=['add_sub'])
async def price(message: types.Message):
    if str(message.from_user.id) == config.BOT_OWNER:
        await AddSubscribe.user.set()
        await message.answer("Кому добавляем подписку?")
    else:
        await message.answer("⚠️ Недостаточно прав!", parse_mode="Markdown")

@dp.message_handler(lambda message: message.text.isdigit(), state=AddSubscribe.user)
async def add_user_sub(message: types.Message, state: FSMContext):
    if not db.user_exists(message.text):
        await message.answer("*Пользователь с данным ID, не найден*", parse_mode="Markdown")
    else:
        async with state.proxy() as data:
            data['user'] = message.text

        await AddSubscribe.next()
        await message.answer("На сколько дней предоставить подписку?", parse_mode="Markdown")

@dp.message_handler(lambda message: message.text.isdigit(), state=AddSubscribe.period)
async def add_period_sub(message: types.Message, state: FSMContext):

    global from_date, status
    async with state.proxy() as data:
            data['period'] = message.text
    
    number_pay = random.randint(1000000000000, 9999999999999)

    if int(data['period']) == 7:
        total_amount = 7900
        status = 'Standard'
        from_date = date.today() + timedelta(days=int(data['period']))

    if int(data['period']) == 30:
        total_amount = 13900
        status = 'Premium'
        from_date = date.today() + timedelta(days=int(data['period']))

    if int(data['period']) == 365:
        total_amount = 59900
        status = 'VIP'
        from_date = date.today() + timedelta(days=int(data['period']))

    db.add_subscribtion(
        int(data['user']),
        date.today(),
        from_date,
        status,
        number_pay
    )

    await bot.send_message(
        message.chat.id,
        f"✅️ Платеж прошел успешно на сумму {total_amount // 100} RUB!"
        f"\nПакет Standart успешно подключен до {from_date}\n\nПриятного общения! 😉", reply_markup=mark_menu)

    await bot.send_message(-1001589390234,
                           f"*Пользователь приобрел подписку:\n\nID:* _{data['user']}_\n*Подписка:* _{status}_"
                           f"\n*Номер заказа:* _{number_pay}_\n*Доход:*" +
                           f"_{total_amount // 100}RUB_", parse_mode="Markdown")

    await bot.send_sticker(-1001589390234, "CAACAgIAAxkBAAIkrmCH4Ezu3k0w_8-0-KvgBtnAPvA8AAJoAAPANk8TTP09o-fEaYcfBA")
    await bot.send_sticker(data['user'],
                           "CAACAgIAAxkBAAIkeGCG4rGz_NC_PCAKw0LTd04Et0WGAALeAANWnb0Kpe93OFWDFcQfBA")