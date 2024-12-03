
import asyncio, sqlite3, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import BOT_TOKEN, SITE_TO_AUTH, SFX_SITE, DATABASES
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, filename='log_tgbot.log',
                    format='%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(msg: types.Message):
    # Получаем токен из сообщения, сформированного Django в броузере пользователя
    # и отрпаваленного пользователем из своей учетной записи Telegram в Telegram-бот
    token = msg.text.partition('/start ')[2]
    try:
        conn = sqlite3.connect(DATABASES)
        cur = conn.cursor()
        # Проверяем есть ли пользователь в базе Django с Telegram-id
        sql = f'SELECT id FROM djauth_user WHERE idtlg = "{msg.from_user.id}";'
        id = cur.execute(f'SELECT id FROM djauth_user WHERE idtlg = "{msg.from_user.id}";').fetchone()
        # Если есть - обновляем ему токен
        if id:
            sql = (f'UPDATE djauth_user SET token = "{token}" WHERE id="{id[0]}";')
            cur.execute(sql)
            conn.commit()
            conn.close()
        # Если пользователя нет - заводим нового, записываем ему токен
        else:
            username = msg.from_user.username
            id = cur.execute(f'SELECT id FROM djauth_user WHERE username = "{username}"').fetchone()
            if id:
                username = username + msg.from_user.id
            sql = (f"""INSERT INTO djauth_user (is_superuser,is_staff, is_active, date_joined,username,first_name,last_name,idtlg,email,token,password)
                        VALUES (1,1,1,'{datetime.now(timezone.utc)}','{username}','{msg.from_user.first_name}','{msg.from_user.last_name}','{msg.from_user.id}',
                        '{str(msg.from_user.id)+SFX_SITE}','{token}','{token}');""")
            cur.execute(sql)
            conn.commit()
            conn.close()
    except Exception as err:
        logging.error(f'sqlite3: {err}')
        # Если ошибка авторизации - сообщаем пользователю в Телеграме
        await msg.answer(f'Ошибка авторизации на сайте {SITE_TO_AUTH}')
    # Сообщаем пользователю в Телеграме об успешной авторизации
    name = f'{msg.from_user.full_name } ({msg.from_user.username})'
    await msg.answer(f'{name}! Вы авторизовались на сайте {SITE_TO_AUTH}')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
