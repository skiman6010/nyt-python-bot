import datetime, logging, pytz, os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    context.job_queue.run_daily(url,
                                datetime.time(hour=6, minute=30, tzinfo=pytz.timezone('US/Eastern')),
                                days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def url(context):
    baseurl = "https://static01.nyt.com/images/"
    file = "nytfrontpage/scan.pdf"
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%Y/%m/%d/")
    formatted_url = baseurl + formatted_date + file

    context.bot.send_message(chat_id = context.job.context, text=formatted_url)


def main():
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start, pass_job_queue=True))
    dp.add_handler(CommandHandler("now", url))
    dp = updater.dispatcher

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()