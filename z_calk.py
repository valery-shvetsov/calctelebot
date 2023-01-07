from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from telegram import Update
from config import TOKEN
from z_func import*

updater=Updater(TOKEN)
dispatcher=updater.dispatcher

conv_handler_rational=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        #NUMBERS: [MessageHandler(Filters.text,numbers)],
        ARGUMENT_A: [MessageHandler(Filters.text,input_a)],
        ARGUMENT_B: [MessageHandler(Filters.text,input_b)],
        ACTION:[MessageHandler(Filters.text,input_action)]
        },
        fallbacks=[CommandHandler('cancel',cancel)],
)

cancel_handler = CommandHandler('cancel',cancel)


dispatcher.add_handler(cancel_handler)
dispatcher.add_handler(conv_handler_rational)


print('Сервер запущен')
updater.start_polling()
updater.idle()

