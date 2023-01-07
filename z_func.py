from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="log_calc.log"
)
logger = logging.getLogger('log_calc')
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()

#NUMBERS, ARGUMENT_A, ARGUMENT_B, ACTION= range(4)
ARGUMENT_A, ARGUMENT_B, ACTION= range(3)

def start(update:Update,_):
    """ 
    Действия после нажатия start
    """
    update.message.reply_text('Вас приветствует калькулятор рациональных чисел \n')
    update.message.reply_text (f'Введите аргумент А')
    return ARGUMENT_A


def input_a (update:Update, context:CallbackContext):
    """
    Ввод аргумента А с логированием
    Перевод его в вещественный тип 
    и назначением глобальной переменной
    Проверка на ввод числа
    """
    mes_a=update.message.text
    user = update.message.from_user
    #print (user)
    logger.info("Arg_A %s: %s", update.message.text, user.username)
    try:
        float(mes_a)
        global argument_a
        argument_a=float(mes_a)
        print(argument_a)
        update.message.reply_text (f'Введите аргумент B')
        return ARGUMENT_B

    except ValueError:
        update.message.reply_text ('Введено не число. \n Повторите ввод аргумента А')

def input_b (update:Update, context:CallbackContext):
    """
    Ввод аргумента В с логированием
    Перевод его в вещественный тип 
    и назначением глобальной переменной
    Создание клавиатуры для ввода действия
    Проверка на ввод числа
    """
    mes_b=update.message.text
    user = update.message.from_user
    logger.info("Arg_B %s: %s", update.message.text, user.username)
    try:
        float(mes_b)
        global argument_b
        argument_b=float(mes_b)
        print(argument_b)
        reply_keyboard = [
        ['a+b', 'a-b'],
        ['a*b', 'a/b'],
        ['a**b', 'a**(1/b)'],
        ]       
        markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(
            'Выберите действие над аргументами.',
            reply_markup=markup_key, )
        return ACTION
    except ValueError:
        update.message.reply_text ('Введено не число. \n Повторите ввод аргумента В')

def input_action (update:Update, context:CallbackContext):
    """
    Выбор действия над аргументами
    Логирование действия
    Анализ действия и выполнение соответствующей операции с аргументами
    Вывод результата и его логирование
    Проверка на деление на 0
    Проверка на отрицательный аргумент корня
    """
    action=update.message.text
    user = update.message.from_user
    logger.info("action %s: %s", update.message.text, user.username)
    a=argument_a
    b=argument_b
    result=0
    if action=='a+b': 
        result=a+b
        update.message.reply_text (f'{a} + {b} = {result}')
        user = update.message.from_user
        msg=f'{a} + {b} = {result} {user.username}'
        logger.info (msg)
    elif action=='a-b': 
        result=a-b
        update.message.reply_text (f'{a} - {b} = {result}')
        user = update.message.from_user
        msg=f'{a} - {b} = {result} {user.username}'
        logger.info (msg)
    elif action=='a*b': 
        result=a*b
        update.message.reply_text (f'{a} * {b} = {result}')
        user = update.message.from_user
        msg=f'{a} * {b} = {result} {user.username}'
        logger.info (msg)
    elif action=='a/b': 
        if b==0:
            result='oo'
            update.message.reply_text (f'{a} / {b} = {result}')
            update.message.reply_text (f'При аргументе B=0, \nдействие не может быть выполнено.')
        else:
            result=a/b
            update.message.reply_text (f'{a} / {b} = {result}')
            user = update.message.from_user
            msg=f'{a} / {b} = {result} {user.username}'
            logger.info (msg)
    elif action=='a**b':
        if a<0 and b<1: 
            update.message.reply_text (f'При аргументе А<0 и аргументе В<1, \nдействие не может быть выполнено.')
        else:
            result=a**b
            update.message.reply_text (f'{a} ** {b} = {result}')
            user = update.message.from_user
            msg=f'{a} ** {b} = {result} {user.username}'
            logger.info (msg)        
    elif action=='a**(1/b)':
        if a<0 and b>1:
            update.message.reply_text (f'При аргументе А<0 и аргументе В>1, \nдействие не может быть выполнено.')
        else: 
            result=a**(1/b)
            update.message.reply_text (f'{a} ** 1/{b} = {result}')
            user = update.message.from_user
            msg=f'{a} **(1/{b}) = {result} {user.username}'
            logger.info (msg)
    
    update.message.reply_text ('Для продолжения вычислений введите /start \n'
                                'Для выхода введите /cancel')
    return ConversationHandler.END


def cancel (update:Update, context:CallbackContext):
    """
    Действия при команде cansel
    """
    update.message.reply_text (f'Работа окончена. \nДля продолжения вычислений введите /start')
    reply_markup=ReplyKeyboardRemove()
    return ConversationHandler. END



