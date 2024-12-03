from tgbot.config import TELEGRAM_BOT_USERNAME

def isauth_f(token):
    # isauth = True
    isauth = False
    return isauth

def bot_req(token):
    bot_link = f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={token}"
    return