from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import Converter
from config import TELEGRAM_TOKEN


def main():
    updater = Updater(TELEGRAM_TOKEN)
    converter = Converter()
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", converter.start))
    dp.add_handler(CommandHandler("values", converter.show_available_currencies))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, converter.convert_currency))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()