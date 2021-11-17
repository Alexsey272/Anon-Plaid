import logging
import dotenv
import os
from database import dbworker
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import *

# время
now = datetime.now()
now = now.strftime("%Y-%m-%d")
now = datetime.strptime(now, '%Y-%m-%d')

dotenv.load_dotenv('.env')

TOKEN = os.environ['TOKEN']
ADMIN = os.environ['ADMINS']
BOT_OWNER = os.environ['BOT_OWNER']
PAYMENTS = os.environ['PAYMENTS']
YANDEX_API = os.environ['YANDEX_API']

#логирование
logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')
warning_log = logging.getLogger("warning_log")
warning_log.setLevel(logging.WARNING)

fh = logging.FileHandler("warning_log.log")

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

warning_log.addHandler(fh)

if not TOKEN:
    exit("No token provided")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage = MemoryStorage())

# инициализируем базу данных
db = dbworker('db dumb1.db')
