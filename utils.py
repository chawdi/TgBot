import requests
from telegram.ext import MessageHandler, Filters

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"https://min-api.cryptocompare.com/data/price"
        params = {
            "fsym": base,
            "tsyms": quote
        }
        response = requests.get(url, params=params)
        data = response.json()
        if quote not in data:
            raise ValueError("Выбранная валюта не поддерживается. Пожалуйста, выберите RUB, USD, EUR, CNY, BTC или ETH.")
        rate = data[quote]
        converted_amount = amount * rate
        return converted_amount

    @staticmethod
    def start(update, context):
        update.message.reply_text("Привет! Я бот для конвертации валют. Отправьте мне сообщение в формате: "
                                  "RUB USD 100")

    @staticmethod
    def convert_currency(update, context):
        try:
            user_input = update.message.text.upper()
            base, quote, amount = user_input.split()
            amount = float(amount)

            converted_amount = Converter.get_price(base, quote, amount)
            update.message.reply_text(f"{amount} {base} равно {converted_amount:.2f} {quote}. ")

            # Добавляем хендлер для обработки ответа пользователя
            dp = context.dispatcher
            dp.add_handler(MessageHandler(Filters.text & ~Filters.command, Converter.continue_handler))

            # Устанавливаем контекст, чтобы в дальнейшем передать результат конвертации и валюты
            context.user_data['converted_amount'] = converted_amount
            context.user_data['base_currency'] = base
            context.user_data['quote_currency'] = quote

        except ValueError as e:
            update.message.reply_text(str(e))

        except Exception:
            update.message.reply_text("Произошла ошибка при конвертации. Пожалуйста, попробуйте еще раз.")

    @staticmethod
    def show_available_currencies(update, context):
        available_currencies = "Доступные валюты: RUB, USD, EUR, CNY, BTC, ETH"
        update.message.reply_text(available_currencies)

    @staticmethod
    def continue_handler(update, context):
        user_input = update.message.text.lower()
        if user_input == 'да':
            update.message.reply_text("Отправьте новое сообщение с другими валютами и суммой.")
            # Удаляем хендлер для ответа пользователя
            dp = context.dispatcher
            dp.remove_handler(Converter.continue_handler)
        else:
            update.message.reply_text("Работа завершена. Чтобы начать новую конвертацию, введите команду /start.")
            # Удаляем хендлер для ответа пользователя
            dp = context.dispatcher
            dp.remove_handler(Converter.continue_handler)
