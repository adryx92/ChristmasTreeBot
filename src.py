#!/usr/bin/python3

import telebot
import emoji

# project dependencies
import const
from rest import RestManager
from db import DatabaseHandler

# users auth
TOKEN = "MYTOKEN"
bot = telebot.TeleBot(TOKEN)

db_handler = DatabaseHandler()
users_list = db_handler.get_users_list()
endpoint_list = db_handler.get_targets_list()

rest = RestManager(endpoint_list)

# global vars
_lastUserAction = None

def get_status_str(isOn, lastUserAction):
	result = ""
	if isOn:
		result = const.MESSAGE_STATUS_ON + " " + emoji.emojize(":bulb:", language='alias')
	else:
		result = const.MESSAGE_STATUS_OFF + " " + emoji.emojize(":red_circle:")

	if lastUserAction != None:
		result += " da " + lastUserAction.full_name

	return result

# custom Telegram keyboard
def create_custom_keyboard():
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(telebot.types.KeyboardButton(const.CMD_ON))
	keyboard.add(telebot.types.KeyboardButton(const.CMD_OFF))
	keyboard.add(telebot.types.KeyboardButton(const.CMD_STATUS))
	return keyboard

def remove_custom_keyboard():
	keyboard = telebot.types.ReplyKeyboardRemove()
	return keyboard

# keyboard messages handler
@bot.message_handler(func=lambda message: message.text in [const.CMD_ON, const.CMD_OFF, const.CMD_STATUS])
def handle_custom_keyboard(message):
	global _lastUserAction
	action = message.text

	is_on = rest.get_status()
	# status is always asked. therefore, if it didn't succeed, it certainly won't be able to do the other operations either
	if is_on == None:
		bot.send_message(message.chat.id, const.MESSAGE_OP_ERROR + " " + emoji.emojize(":face_with_crossed_out_eyes:", language='alias'))
		return

	if action == const.CMD_STATUS:
		bot.send_message(message.chat.id, get_status_str(is_on, _lastUserAction))
		return
	else:
		if ((action == const.CMD_ON and is_on) or (action == const.CMD_OFF and not is_on)):
			bot.send_message(message.chat.id, "Già " + get_status_str(is_on, _lastUserAction))
			return
		else:
			result = None
			if action == const.CMD_ON:
				result = rest.turn_all_on()
			elif action == const.CMD_OFF:
				result = rest.turn_all_off()

			if result == None:
				bot.send_message(message.chat.id, const.MESSAGE_OP_ERROR + " " + emoji.emojize(":face_with_crossed_out_eyes:", language='alias'))
				return

			if action == const.CMD_ON:
				bot.send_message(message.chat.id, const.MESSAGE_STATUS_ON + " " + emoji.emojize(":white_check_mark:", language='alias'))
			elif (action == const.CMD_OFF):
				bot.send_message(message.chat.id, const.MESSAGE_STATUS_OFF + " " + emoji.emojize(":white_check_mark:", language='alias'))

			_lastUserAction = message.from_user
			db_handler.add_log(message.from_user.id, str(message.from_user), message.text)

# command messages handler
@bot.message_handler(commands=const.ACCEPTED_COMMANDS)
def handle_command(message):
	global _lastUserAction

	if message.from_user.id not in users_list:
		bot.reply_to(message, const.MESSAGE_UNKNOWN_USER)
		db_handler.add_log(message.from_user.id, str(message.from_user), message.text)
		return
	
	command = message.text

	if command == "/" + const.CMD_START:
		bot.reply_to(message, const.MESSAGE_HELP, reply_markup=create_custom_keyboard())
	elif command == "/" + const.CMD_STOP:
		bot.reply_to(message, "Usa /start per riavviare", reply_markup=remove_custom_keyboard())

	db_handler.add_log(message.from_user.id, str(message.from_user), message.text)

bot.infinity_polling()
