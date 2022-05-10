import requests


class ConnectorInterface:
	SUFFIX: str
	PORT: int
	SERVER_ADDR: str
	USERNAME: str
	PASSWORD: str
	API_KEY: str = None

	def __init__(self):
		self._authenticate()

	def _get(self, url: str, params: dict = None):
		headers = {}
		if self.API_KEY is not None:
			headers['Authorization'] = self.API_KEY

		return requests.get(url=url, params=params, headers=headers).json()

	def _post(self, url: str, data: dict):
		headers = {'Content-Type': 'application/json'}
		if self.API_KEY is not None:
			headers['Authorization'] = self.API_KEY

		response = requests.post(url=url, json=data, headers=headers)
		if response.status_code == 200:
			return response.json()
		if response.status_code >= 300:
			raise Exception('Post unsuccessful ({}): {}'.format(response.status_code, response.text))

	def _authenticate(self):
		""" Authenticate with the API server """
		pass

	def upload_proposal(self, data: dict):
		""" Upload a single proposal """
		pass

	def upload_sample(self, data: dict):
		""" Upload a single sample """
		pass

	def upload_dataset(self, data: dict):
		""" Upload a single raw_dataset/measurement """
		pass

	def upload_proposals(self, data: list):
		""" Upload multiple proposals """
		for entry in data:
			self.upload_proposal(entry)

	def upload_samples(self, data: list):
		""" Upload multiple samples """
		for entry in data:
			self.upload_sample(entry)

	def upload_datasets(self, data: list):
		""" Upload multiple raw_datasets/measurements """
		for entry in data:
			self.upload_dataset(entry)
