from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

log_btn = InlineKeyboardButton('Логи', callback_data = 'log')
add_admin_btn = InlineKeyboardButton('Добавить админа', callback_data = 'add_admin')
del_admin_btn = InlineKeyboardButton('Удалить админа', callback_data = 'del_admin')
add_ban_btn = InlineKeyboardButton('Заблокировать', callback_data = 'ban')
del_ban_btn = InlineKeyboardButton('Разблокировать', callback_data = 'unban')
all_admin_btn = InlineKeyboardButton('Список админов', callback_data = 'all_admin')
admin_menu = InlineKeyboardMarkup().add(log_btn, all_admin_btn).add(add_admin_btn, del_admin_btn).add(add_ban_btn, del_ban_btn)

cancel_btn = InlineKeyboardButton(' Отменить', callback_data = 'cancel')
cancel_menu = InlineKeyboardMarkup().add(cancel_btn)

channel_btn = InlineKeyboardButton('Перейти в канал', url = "https://t.me/CrimsonNews")
channel_menu = InlineKeyboardMarkup().add(channel_btn)

confirm = KeyboardButton('С правилами ознакомлен ✅️')
confirm_button = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
confirm_button.add(confirm)

inline_report_btn = InlineKeyboardButton('Пожаловаться ➡️', callback_data='report')
like_btn = InlineKeyboardButton('👍', callback_data='like')
dislike_btn = InlineKeyboardButton('👎', callback_data='dislike')

menu_like = InlineKeyboardMarkup().add(like_btn, dislike_btn).add(inline_report_btn)

edit_vk = InlineKeyboardButton('VK', callback_data='edit_vk')
edit_instagram = InlineKeyboardButton('Instagram', callback_data='edit_instagram')
menu_social = InlineKeyboardMarkup().add(edit_vk, edit_instagram)

edit_male = InlineKeyboardButton('Парень', callback_data='edit_male')
edit_female = InlineKeyboardButton('Девушка', callback_data='edit_female')
cancel_stg = InlineKeyboardButton('Вернуться', callback_data = 'stg_cancel')
edit_sex = InlineKeyboardMarkup().add(edit_male, edit_female).add(cancel_stg)

stg_sex = InlineKeyboardButton('Пол', callback_data = 'stg_edit_sex')
settings_menu = InlineKeyboardMarkup().add(stg_sex).add(cancel_btn)

link_btn_insta = InlineKeyboardButton('insta', callback_data='insta')
link_btn_vk = InlineKeyboardButton('Vk', callback_data='vk')
link_btn_tg = InlineKeyboardButton('Telegram', callback_data='link')
link_btn_tg_fall = InlineKeyboardButton('Отменить', callback_data = 'not_link')
link_menu = InlineKeyboardMarkup().add(link_btn_tg, link_btn_vk, link_btn_insta).add(link_btn_tg_fall)

inline_spam = InlineKeyboardButton('Спам 📢', callback_data='spam')
inline_sale = InlineKeyboardButton('Продажа 💲', callback_data = 'sale')
inline_porno = InlineKeyboardButton('Порнография 🔞', callback_data='porno')
inline_insult = InlineKeyboardButton('Оскорбление 🤬', callback_data = 'insult')
inline_back = InlineKeyboardButton('Назад 🔙', callback_data = 'back')
inline_report = InlineKeyboardMarkup().add(inline_spam, inline_sale).add(inline_porno, inline_insult).add(inline_back)



button_search = KeyboardButton('Начать поиск 🔍')
buy = KeyboardButton('Подписка 💲')


mark_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mark_menu.add(button_search).add(buy)


stop = KeyboardButton('❌Остановить диалог')
share_link = KeyboardButton('✉️ Отправить ссылку на себя')
m = KeyboardButton('М')
w = KeyboardButton('Д')

menu_msg = ReplyKeyboardMarkup(resize_keyboard=True)
menu_msg.add(stop).add(m,w).add(share_link)


male = KeyboardButton('Парня 👨')
wooman = KeyboardButton('Девушку 👩')

sex_search = KeyboardButton('Поиск по полу 👫')
random_btn = KeyboardButton('Рандомный поиск 🔎')
back = KeyboardButton('Назад 🔙')

search_menu = ReplyKeyboardMarkup(resize_keyboard=True)
search_menu.add(random_btn).add(sex_search).add(back)

sex_menu = ReplyKeyboardMarkup(resize_keyboard=True)
sex_menu.add(male,wooman).add(back)

seven_day = KeyboardButton('79₽ за 7 дней')
one_month = KeyboardButton('130₽ за 30 дней')
one_year = KeyboardButton('599₽ за 365 дней')
back_pay = KeyboardButton('Назад 🔙')

subscription_menu = ReplyKeyboardMarkup(resize_keyboard=True)
subscription_menu.add(seven_day).add(one_month).add(one_year).add(back_pay)

my_sex1 = KeyboardButton('Парень 👨')
my_sex0 = KeyboardButton('Девушка 👩')

my_sex = ReplyKeyboardMarkup(resize_keyboard=True)
my_sex.add(my_sex0, my_sex1)

btn_location = KeyboardButton("Поделится местоположением ", request_location=True)
btn_back = KeyboardButton("Назад 🔙")
location_menu = ReplyKeyboardMarkup(resize_keyboard=True)
location_menu.add(btn_location).add(btn_back)

select_one = KeyboardButton("1")
select_two = KeyboardButton("2")
select_three = KeyboardButton("3")
select_four = KeyboardButton("4")
select_five = KeyboardButton("5")
back = KeyboardButton('Назад 🔙')
select_menu = ReplyKeyboardMarkup(resize_keyboard=True)
select_menu.row(select_one,select_two,select_three,select_four, select_five).add(back)