BOT_TOKEN = '--------' #Tgstat777Bot
TELEGRAM_BOT_USERNAME = 'Tgstat777Bot'
SITE_TO_AUTH = "https://tgstat.ru/"
SFX_SITE = "@tgstat.ru"

from os.path import abspath, dirname, join
BASE_DIR = dirname(dirname(abspath(__file__)))
DATABASES = join(BASE_DIR, 'db.sqlite3')
