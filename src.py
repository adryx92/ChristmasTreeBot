#!/usr/bin/python3

import telebot
import datetime
import logging
import requests
import emoji
import enum
import json

# constants definition
TOKEN = "MYTOKEN"
MESSAGE_UNKNOWN_USER = "Non sei autorizzato a utilizzare questo Bot"
MESSAGE_HELP = "Usa i pulsanti per accendere, spegnere e controllare lo stato del Bot"
MESSAGE_OP_ERROR = "Errore nella richiesta"
MESSAGE_STATUS_ON = "Acceso"
MESSAGE_STATUS_OFF = "Spento"
UNKNOWN_LOG_FILENAME = "unknown_users.log"
LOG_FILENAME = "users.log"
CMD_ON = "Accendi"
CMD_OFF = "Spegni"
CMD_STATUS = "Stato"
CMD_STOP = "stop"
CMD_START = "start"
ACCEPTED_COMMANDS = [CMD_STOP, CMD_START]
IP_LIST = [
	# {'addr': '10.0.1.164', 'api_ver': 2},
	{'addr': '10.0.1.166', 'api_ver': 2},
	{'addr': '10.0.1.167', 'api_ver': 1},
]
bot = telebot.TeleBot(TOKEN)

# users auth
USER_FRA = 1234
USER_PINU = 1234
USER_ANTO = 1234
AUTH_USERS = [USER_FRA, USER_PINU, USER_ANTO]

# global vars
_lastUserAction = None

class ApiEndpoint(enum.Enum):
	RELAY = "relay"
	STATUS = "status"

def make_http_request(endpoint, target, status=None):
	if endpoint not in ApiEndpoint.__members__.values():
		raise ValueError("Endpoint non valido")

	base_url = f'http://{target["addr"]}'

	# build URL
	if (target['api_ver'] == 1):
		if endpoint == ApiEndpoint.RELAY:
			url = f'{base_url}/relay/0?turn={"on" if status else "off"}'
		elif endpoint == ApiEndpoint.STATUS:
			url = f'{base_url}/status/0'
	elif (target['api_ver'] == 2):
		if endpoint == ApiEndpoint.RELAY:
			# the OLD API is still compatible
			# url = f'{base_url}/rpc/Switch.Set?id=0&on={str(status).lower()}'
			url = f'{base_url}/relay/0?turn={"on" if status else "off"}'
		elif endpoint == ApiEndpoint.STATUS:
			url = f'{base_url}/rpc/Switch.GetStatus?id=0'
	else:
		raise ValueError("Endpoint non supportato")

	# GET request
	try:
		# since requests are made in LAN, 2 seconds of timeout are enough
		response = requests.get(url, timeout=2)

		if response.status_code == 200:
			if (endpoint == ApiEndpoint.RELAY):
				return True
			else:
				return json.loads(response.text)
		else:
			print(f'Errore nella richiesta GET. Codice di stato: {response.status_code}')
			return False
	except requests.exceptions.RequestException as e:
		print(f'Errore nella richiesta GET: {e}')
		return False

def turn_on_off(statusOn):
	results = []
	for target in IP_LIST:
		success = make_http_request(ApiEndpoint.RELAY, target, statusOn)
		results.append(success)

	if False in results:
		return False
	else:
		return True

def turn_all_on():
	return turn_on_off(True)

def turn_all_off():
	return turn_on_off(False)

def get_status():
	results = []
	for target in IP_LIST:
		response = make_http_request(ApiEndpoint.STATUS, target)
		if (target['api_ver'] == 1):
			results.append(response['relays'][0]['ison'])
		elif (target['api_ver'] == 2):
			results.append(response['output'])

	if False in results:
		return False
	else:
		return all(results)

def get_status_str(isOn, lastUserAction):
	result = ""
	if isOn:
		result = MESSAGE_STATUS_ON + " " + emoji.emojize(":bulb:", language='alias')
	else:
		result = MESSAGE_STATUS_OFF + " " + emoji.emojize(":red_circle:")

	if lastUserAction != None:
		result += " da " + lastUserAction.full_name

	return result

# custom Telegram keyboard
def create_custom_keyboard():
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(telebot.types.KeyboardButton(CMD_ON))
	keyboard.add(telebot.types.KeyboardButton(CMD_OFF))
	keyboard.add(telebot.types.KeyboardButton(CMD_STATUS))
	return keyboard

def remove_custom_keyboard():
	keyboard = telebot.types.ReplyKeyboardRemove()
	return keyboard

# keyboard messages handler
@bot.message_handler(func=lambda message: message.text in [CMD_ON, CMD_OFF, CMD_STATUS])
def handle_custom_keyboard(message):
	global _lastUserAction
	action = message.text

	is_on = get_status()
	# status is always asked. therefore, if it didn't succeed, it certainly won't be able to do the other operations either
	if is_on == None:
		bot.send_message(message.chat.id, MESSAGE_OP_ERROR + " " + emoji.emojize(":face_with_crossed_out_eyes:", language='alias'))
		return

	if action == CMD_STATUS:
		bot.send_message(message.chat.id, get_status_str(is_on, _lastUserAction))
		return
	else:
		if ((action == CMD_ON and is_on) or (action == CMD_OFF and not is_on)):
			bot.send_message(message.chat.id, "Già " + get_status_str(is_on, _lastUserAction))
			return
		else:
			result = None
			if action == CMD_ON:
				result = turn_all_on()
			elif action == CMD_OFF:
				result = turn_all_off()

			if result == None:
				bot.send_message(message.chat.id, MESSAGE_OP_ERROR + " " + emoji.emojize(":face_with_crossed_out_eyes:", language='alias'))
				return

			if action == CMD_ON:
				bot.send_message(message.chat.id, MESSAGE_STATUS_ON + " " + emoji.emojize(":white_check_mark:", language='alias'))
			elif (action == CMD_OFF):
				bot.send_message(message.chat.id, MESSAGE_STATUS_OFF + " " + emoji.emojize(":white_check_mark:", language='alias'))

			_lastUserAction = message.from_user

# command messages handler
@bot.message_handler(commands=ACCEPTED_COMMANDS)
def handle_command(message):
	global _lastUserAction

	curDate = datetime.datetime.now().strftime("%Y/%m/%d - %T")

	if message.from_user.id not in AUTH_USERS:
		bot.reply_to(message, MESSAGE_UNKNOWN_USER)
		logging.basicConfig(filename=UNKNOWN_LOG_FILENAME)
		logging.warning(f"[{curDate}] - USER {str(message.from_user)}] - MSG \"{message.text}\"")
		return
	
	command = message.text

	if command == "/" + CMD_START:
		bot.reply_to(message, MESSAGE_HELP, reply_markup=create_custom_keyboard())
	elif command == "/" + CMD_STOP:
		bot.reply_to(message, "Usa /start per riavviare", reply_markup=remove_custom_keyboard())

	logging.basicConfig(filename=LOG_FILENAME)
	logging.warning(f"[{curDate}] - USER {str(message.from_user)}] - MSG \"{message.text}\"")

bot.infinity_polling()
