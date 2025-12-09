import requests
import telebot

TOKEN = ""

class ClientNBRB:
    def __init__(self):
        self.USD_URL = requests.get("https://api.nbrb.by/exrates/rates/431").json()
        self.EUR_URL = requests.get("https://api.nbrb.by/exrates/rates/451").json()

    def get_usd_rate(self):
        if self.USD_URL:
            return self.USD_URL["Cur_OfficialRate"]
        return None

    def get_eur_rate(self):
        if self.EUR_URL:
            return self.EUR_URL["Cur_OfficialRate"]
        return None

class CurrencyBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.client = ClientNBRB()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id,
                "Привет! Введите сумму в белорусских рублях (BYN),\n"
                "и я переведу её в USD и EUR по курсу НБРБ.")

        @self.bot.message_handler(func=lambda msg: True)
        def handle_message(message):
            try:
                amount = float(message.text)
                if amount <= 0:
                    self.bot.reply_to(message, "Введите положительное число.")
                    return
            except ValueError:
                self.bot.reply_to(message, "Введите число, например: 10")
                return

            usd_rate = self.client.get_usd_rate()
            eur_rate = self.client.get_eur_rate()

            if not usd_rate or not eur_rate:
                self.bot.reply_to(message, "Ошибка: не удалось получить курс. Проверьте подключение.")
                return

            usd_amount = amount / usd_rate
            eur_amount = amount / eur_rate

            result = (
                f"{amount:.2f} BYN =\n\n"
                f" {usd_amount:.4f} USD\n"
                f"   (1 USD = {usd_rate:.4f} BYN)\n\n"
                f" {eur_amount:.4f} EUR\n"
                f"   (1 EUR = {eur_rate:.4f} BYN)")
            self.bot.reply_to(message, result)
    def run(self):
        print(" Бот запущен... Ожидание сообщений.")
        self.bot.polling()



if __name__ == "__main__":

    bot = CurrencyBot(TOKEN)
    bot.run()




