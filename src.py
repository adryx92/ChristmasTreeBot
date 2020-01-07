import telebot
import datetime
import logging
from telebot import types
from gpiozero import LED
from threading import Timer
import emoji

# constants definition
TOKEN = "MYTOKEN"
MESSAGE_UNKNOWN_USER = "Non sei autorizzato a utilizzare questo Bot"
MESSAGE_HELP = "Usa i comandi /accendi, /spegni e /stato per utilizzare il Bot"
MESSAGE_CONFIRMATION = "Effettuato"
MESSAGE_STATUS_ON = "acceso"
MESSAGE_STATUS_OFF = "spento"
LOG_FILENAME = "unknown_users.log"
CMD_ON = "/accendi"
CMD_OFF = "/spegni"
CMD_STATUS = "/stato"
CMD_HELP = "/help"
CMD_START = "/start"
CMD_TIMER = "/timer"
ACCEPTED_COMMANDS = ['start', 'help', 'accendi', 'spegni', 'stato', 'timer']
bot = telebot.TeleBot(TOKEN)
rel1 = LED(26)

# users auth
USER_FRA = 1234
USER_PINU = 1234
USER_ANTO = 1234
AUTH_USERS = [USER_FRA, USER_PINU, USER_ANTO]

# global vars
_status = 0
_lastUserAction = None


def exec_command(cmd):
    if cmd == CMD_ON:
        turn_on()
    elif cmd == CMD_OFF:
        turn_off()
    elif cmd == CMD_TIMER:
        timer()

def turn_on():
    rel1.on()
    global _status
    _status = 1
    
def turn_off():
    rel1.off()
    global _status
    _status = 0
    
def timer():
    global _status
    if(_status == 0):
        turn_on()
    # after 10 seconds, turn it off
    t = Timer(10.0, turn_off)
    t.start()
    

def get_status_str():
    global _status
    if _status == 1:
        return MESSAGE_STATUS_ON + " " + emoji.emojize(":bulb:", use_aliases=True)
    else:
        return MESSAGE_STATUS_OFF + " " + emoji.emojize(":red_circle:")
   
# bot commands
@bot.message_handler(commands=ACCEPTED_COMMANDS)
def handle_command(message):
    global _lastUserAction

    if message.from_user.id in AUTH_USERS:
        if (message.text == CMD_START or message.text == CMD_HELP):
            bot.reply_to(message, MESSAGE_HELP)
        elif (message.text == CMD_STATUS):
            if (_lastUserAction != None):
                bot.reply_to(message, 'Albero {} da {}'.format(get_status_str(), _lastUserAction.first_name))
            else:
                bot.reply_to(message, get_status_str().title())
        else:
            if ((message.text == CMD_ON and _status == 1) or (message.text == CMD_OFF and _status == 0) and _lastUserAction != None):
                bot.reply_to(message, 'Albero già {} da {}'.format(get_status_str(), _lastUserAction.first_name))
            else:
                exec_command(message.text)
                _lastUserAction = message.from_user
                bot.reply_to(message, MESSAGE_CONFIRMATION + " " + emoji.emojize(":white_check_mark:", use_aliases=True))
    else:
        bot.reply_to(message, MESSAGE_UNKNOWN_USER)
        # logging info on the unknown user
        logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
        curDate = datetime.datetime.now().strftime("%A %Y/%m/%d - %T")
        logging.info(" REQUEST_TIME [" + curDate + "], USER [" + str(message.from_user) + "]")

bot.polling()
