import telebot
from telebot import types
from gpiozero import LED

# constants definition
TOKEN = "MYTOKEN"
MESSAGE_UNKNOWN_USER = "Non sei autorizzato a utilizzare questo Bot"
MESSAGE_HELP = "Usa i comandi /accendi, /spegni e /stato per utilizzare il Bot"
USER_FRA = 1234
USER_PINU = 1234
USER_ANTO = 1234
AUTH_USERS = [USER_FRA, USER_PINU, USER_ANTO]
bot = telebot.TeleBot(TOKEN)

status = 0

rel1 = LED(13)
rel2 = LED(19)
rel3 = LED(26)

def exec_command(cmd):
    if cmd == "/accendi":
        turn_on()
    elif cmd == "/spegni":
        turn_off()
    return True

def turn_on():
    rel1.on()
    rel2.on()
    rel3.on()
    global status
    status = 1 
    
def turn_off():
    rel1.off()
    rel2.off()
    rel3.off()
    global status
    status = 0

def get_status():
    return "Acceso" if status == 1 else "Spento"

# bot commands
@bot.message_handler(commands=['start', 'help', 'accendi', 'spegni', 'stato'])
def handle_command(message):
    if message.from_user.id in AUTH_USERS:
        if (message.text == '/start' or message.text == '/help'):
            bot.reply_to(message, MESSAGE_HELP)
        elif (message.text == "/stato"):
            result = get_status()
            bot.reply_to(message, result)
        else:
            result = exec_command(message.text)
            bot.reply_to(message, "Effettuato" if result else "Errore")
    else:
        bot.reply_to(message, MESSAGE_UNKNOWN_USER)

bot.polling()
