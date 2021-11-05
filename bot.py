import os
from telegram.ext import Updater, CommandHandler



t = Test()

def callback_alarm(context):
    job = context.job
    a = t.check()
    if a:
        context.bot.send_message(job.context, text=a)


def reminder(update,context):
    update.message.reply_text(text='Daily reminder has been set! You\'ll get notified at 8 AM daily')
    context.job_queue.run_repeating(callback_alarm, 1, context=update.message.chat_id)


def main():
    """Run the bot."""
    # Create the Updater and pass it your bot's token.


    updater = Updater(os.environ['TOKEN'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("test", reminder))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
