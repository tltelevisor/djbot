BOT_TOKEN = '7405884297:AAH9zFadT60qp4f8pu_Nb3QlzUMsydxPlps' #Tgstat777Bot
TELEGRAM_BOT_USERNAME = 'Tgstat777Bot'
id_admin = 391497468 #Maxim Chakhovsky
SITE_TO_AUTH = "https://tgstat.ru/"
SFX_SITE = "@tgstat.ru"

from os.path import abspath, dirname, join
BASE_DIR = dirname(dirname(abspath(__file__)))
DATABASES = join(BASE_DIR, 'db.sqlite3')