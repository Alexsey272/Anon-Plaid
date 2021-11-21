from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
ADMIN = env.list('ADMINS')
BOT_OWNER = env.str('BOT_OWNER')
PAYMENTS = env.str('PAYMENTS')
YANDEX_API = env.str('YANDEX_API')

REPORT = env.str('REPORT')
ERROR = env.str('ERROR')
DIALOG = env.str('DIALOG')
SUBSCRIBE = env.str('SUBSCRIBE')