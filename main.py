import telebot
from handlers import add_handlers
from config import TOKEN
from i18n import set_language

# Установка языка
set_language('ru')  # Или 'en' для английского

class Bot:
    def __init__(self, token):
        self.token = token

    def start(self):
        while True:
            try:
                self.bot = telebot.TeleBot(self.token)
                add_handlers(self.bot)
                self.bot.polling(none_stop=True)
            except Exception as e:
                print("Произошла ошибка:", e)
                print("Перезапуск бота через 20 минут.")
                import time
                time.sleep(12)  # 12 сек

if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.start()
