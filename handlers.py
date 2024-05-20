from telebot import types
from check_calendar import check_calendar
from create_shift_button import create_shift_event
from allowed_users import allowed_users
import datetime
from i18n import translate as _

def log_user_action(username, action, timestamp):
    with open("user_actions.txt", "a") as file:
        file.write(f"[{timestamp}] Пользователь {username} выполнил действие: {action}\n")

def add_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(_("👋 Поздороваться"))
        btn2 = types.KeyboardButton(_("Работа"))
        user_markup.add(btn1, btn2)

        if message.from_user.username in allowed_users:
            btn3 = types.KeyboardButton(_("Создать смену"))
            user_markup.add(btn3)

        bot.send_message(message.chat.id, _("👋 Привет! Я твой бот-помощник в СТО. Ваше имя пользователя: {username}").format(username=message.from_user.username), reply_markup=user_markup)

    @bot.message_handler(func=lambda message: message.text == _("👋 Поздороваться"))
    def greet(message):
        bot.send_message(message.chat.id, _("Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\"."))

    @bot.message_handler(func=lambda message: message.text == _("Работа"))
    def check_calendar_handler(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_user_action(message.from_user.username, "нажал кнопку 'Работа'", timestamp)
            check_calendar(bot, message)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, _("Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут."))

    @bot.message_handler(func=lambda message: message.text == _("Создать смену"))
    def create_shift(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_user_action(message.from_user.username, "нажал кнопку 'Создать смену'", timestamp)
            bot.send_message(message.chat.id, _("На какую дату вы хотите создать смену (дд-мм-гггг, Например: 01-01-2024)?"))
            bot.register_next_step_handler(message, ask_date)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, _("Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут."))

    def ask_date(message):
        date = message.text
        bot.send_message(message.chat.id, _("Напишите тему смены:"))
        bot.register_next_step_handler(message, lambda message: ask_summary(message, date))

    def ask_summary(message, date):
        summary = message.text
        try:
            create_shift_event(bot, message, date, summary)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, _("Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут."))
