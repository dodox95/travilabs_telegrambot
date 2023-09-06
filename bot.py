import logging
import requests
import json
from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters, CallbackContext, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = ''

# Function responsible for retrieving the coin price.
def get_price(symbol: str) -> float:
    url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol.upper()}&tsyms=USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        if "USD" in data:
            return data["USD"]
        else:
            return None
    else:
        return None

# Handler to get the cryptocurrency price.
def crypto_price(update: Update, context: CallbackContext) -> None:
    # First check if the message starts with '/'
    if not update.message.text.startswith('/'):
        return

    command = update.message.text[1:].lower()  # remove the '/' and convert to lowercase
    price = get_price(command)
    if price:
        update.message.reply_text(f"The current price of {command.upper()} is ${price}")
    else:
        update.message.reply_text(f"Couldn't fetch the price for {command.upper()}. It might be unsupported or there was an error.")

def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Initialize Updater
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register message handler with a filter for text messages starting with '/'
    dp.add_handler(MessageHandler(Filters.command, crypto_price))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    logger.info("Bot is starting...")
    updater.start_polling()
    logger.info("Bot has started.")
    updater.idle()
    logger.info("Bot is ending...")

if __name__ == '__main__':
    main()
