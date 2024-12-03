
# from django.contrib.auth import get_user_model
# User = get_user_model()

import asyncio
import sqlite3
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import BOT_TOKEN, SITE_TO_AUTH, SFX_SITE, DATABASES
from datetime import datetime, timezone
# from handlers import router

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, filename="log_tgbot.log",
                    format="%(asctime)s %(levelname)s %(message)s")
# logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start


@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    # await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
    token = msg.text.partition('/start ')[2]

    try:
        conn = sqlite3.connect(DATABASES)
        cur = conn.cursor()
        logging.info(f"msg.from_user.id: {msg.from_user.id}")
        sql = f"SELECT id FROM djauth_user WHERE idtlg = '{msg.from_user.id}';"
        logging.info(f"sql: {sql}")
        id = cur.execute(f"SELECT id FROM djauth_user WHERE idtlg = '{msg.from_user.id}';").fetchone()
        logging.info(f"id: {id}")
        if id:
            sql = (f"UPDATE djauth_user SET token = '{token}' WHERE id='{id[0]}';")
            cur.execute(sql)
            conn.commit()
            conn.close()
        else:
            username = msg.from_user.username
            id = cur.execute(f"SELECT id FROM djauth_user WHERE username = '{username}'").fetchone()
            if id:
                username = username + msg.from_user.id
            sql = (f"""INSERT INTO djauth_user (is_superuser,is_staff, is_active, date_joined,username,first_name,last_name,idtlg,email,token,password)
                        VALUES (1,1,1,'{datetime.now(timezone.utc)}','{username}','{msg.from_user.first_name}','{msg.from_user.last_name}','{msg.from_user.id}',
                        '{str(msg.from_user.id)+SFX_SITE}','{token}','{token}');""")
            logging.info(sql)
            cur.execute(sql)
            conn.commit()
            conn.close()
    except Exception as err:
        logging.error(f"sqlite3: {err}")
    name = msg.from_user.full_name + " (" + msg.from_user.username + ") "
    await msg.answer(f"{name}! Вы авторизовались на сайте {SITE_TO_AUTH}")

# @dp.message(Command("start"))
# async def cmd_start(msg: types.Message):
#     # await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
#     token = msg.text.partition('/start ')[2]
#     user = User.objects.filter(idtlg=msg.from_user.id)
#     if user:
#         user.token = token
#     else:
#         username = msg.from_user.username
#         if User.objects.filter(username=username): username = username + msg.from_user.id
#         user = User.objects.create_user(username=username,
#                                         first_name=msg.from_user.first_name,
#                                         last_name=msg.from_user.last_name,
#                                         idtlg=msg.from_user.id,
#                                         email=msg.from_user.id+SFX_SITE,
#                                         token=token,
#                                         password=token)
#     logging.info("user: ", user)
#     logging.info(msg.from_user.full_name, msg.from_user.username, msg.from_user.id )
#     name = msg.from_user.full_name + " (" + msg.from_user.username + ") "
#     await msg.answer(f"{name}! Вы авторизовались на сайте {SITE_TO_AUTH}")


# Запуск процесса поллинга новых апдейтов
async def main():
    # dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
