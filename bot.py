import telebot

TOKEN = ""

bot = telebot.TeleBot(TOKEN)
from telebot import types

account_info = {"balance": 2000}
history = []
PIN_CODE = "1234"
authorized = False
action = None
# Проверка PIN
@bot.message_handler(commands=['start'])
def start(message):
    global authorized
    authorized = False
    bot.send_message(message.chat.id, "Введите PIN-код:")

@bot.message_handler(func=lambda m: not authorized)
def check_pin(message):
    global authorized
    if message.text == PIN_CODE:
        authorized = True
        bot.send_message(message.chat.id, "Доступ разрешён")
        show_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, " Неверный PIN. Попробуйте снова.")

# Меню через reply клавиатуру
def show_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Проверить баланс", "Пополнить счёт")
    keyboard.add("Снять средства", "История операций")
    keyboard.add("Выход")
    bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: authorized)
def menu_handler(message):
    global action
    if message.text == "Проверить баланс":
        bot.send_message(message.chat.id, f"Ваш баланс: {account_info['balance']} у.е.")
    elif message.text == "Пополнить счёт":
        bot.send_message(message.chat.id, "Введите сумму для пополнения:")
        action = "deposit"
    elif message.text == "Снять средства":
        bot.send_message(message.chat.id, "Введите сумму для снятия:")
        action = "withdraw"
    elif message.text == "История операций":
        if history:
            bot.send_message(message.chat.id, "\n".join(history))
        else:
            bot.send_message(message.chat.id, "История пуста.")
    elif message.text == "Выход":
        bot.send_message(message.chat.id, "До свидания!", reply_markup=types.ReplyKeyboardRemove())
        authorized = False
    else:
        if action == "deposit":
            try:
                amount = float(message.text)
                account_info["balance"] += amount
                history.append(f"Пополнение: {amount}")
                bot.send_message(message.chat.id, f"Пополнение успешно. Баланс: {account_info['balance']}")
            except:
                bot.send_message(message.chat.id, "Введите корректное число.")
            action = None
        elif action == "withdraw":
            try:
                amount = float(message.text)
                if amount <= account_info["balance"]:
                    account_info["balance"] -= amount
                    history.append(f"Снятие: {amount}")
                    bot.send_message(message.chat.id, f"Снятие успешно. Баланс: {account_info['balance']}")
                else:
                    bot.send_message(message.chat.id, "Недостаточно средств.")
            except:
                bot.send_message(message.chat.id, "Введите корректное число.")
            action = None

bot.polling()