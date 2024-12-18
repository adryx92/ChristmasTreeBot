import enum
import json
import requests
import const

class ApiEndpoint(enum.Enum):
	RELAY = "relay"
	STATUS = "status"

class RestManager:
	def __init__(self, endpoint_list):
		self.endpoint_list = endpoint_list

	def make_http_request(self, endpoint, target, status=None):
		if not isinstance(endpoint, ApiEndpoint):
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

	def turn_on_off(self, statusOn):
		results = []
		for target in self.endpoint_list:
			success = self.make_http_request(ApiEndpoint.RELAY, target, statusOn)
			results.append(success)

		if False in results:
			return False
		else:
			return True

	def turn_all_on(self):
		return self.turn_on_off(True)

	def turn_all_off(self):
		return self.turn_on_off(False)

	def get_status(self):
		results = []
		for target in self.endpoint_list:
			response = self.make_http_request(ApiEndpoint.STATUS, target)
			if (target['api_ver'] == 1):
				results.append(response['relays'][0]['ison'])
			elif (target['api_ver'] == 2):
				results.append(response['output'])

		if False in results:
			return False
		else:
			return all(results)