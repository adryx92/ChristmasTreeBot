# users auth
USER_FRA = 1234
USER_PINU = 1234
USER_ANTO = 1234
TOKEN = "MYTOKEN"

IP_LIST = [
	# {'addr': '10.0.1.164', 'api_ver': 2},
	{'addr': '10.0.1.166', 'api_ver': 2},
	{'addr': '10.0.1.167', 'api_ver': 1},
]

AUTH_USERS = [USER_FRA, USER_PINU, USER_ANTO]

# constants definition
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