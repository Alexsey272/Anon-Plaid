from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# класс машины состояний
class Chating(StatesGroup):
    msg = State()

class Form(StatesGroup):
    vk = State()
    insta = State()
    city = State()
    nickname = State()
    photo = State()

class Register(StatesGroup):
    confirm = State()
    sex = State()

class Account(StatesGroup):
    select = State()


class Report(StatesGroup):
    info = State()


class Block(StatesGroup):
    user = State()
    cause = State()
    time = State()


class Unblock(StatesGroup):
    user = State()


class SendMessage(StatesGroup):
    user = State()
    msg = State()


class AllMessage(StatesGroup):
    msg = State()


class Admin(StatesGroup):
    user = State()


class AdminDel(StatesGroup):
    user = State()

class AddSubscribe(StatesGroup):
    user = State()
    period = State()