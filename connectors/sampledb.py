from connectors.connector_interface import ConnectorInterface


class SampleDB(ConnectorInterface):
	SUFFIX = 'sampledb'
	PORT = 8000
	SERVER_ADDR = 'http://localhost:{}/api/v1'.format(PORT)
	API_KEY = 'Bearer {}'.format('abcd' * 16)

	def __init__(self):
		super().__init__()
		self.url = '{}/objects/'.format(self.SERVER_ADDR)
		self.actions = {}
		self.get_actions()

	def __repr__(self):
		return 'SampleDB'

	def get_actions(self):
		url = '{}/actions'.format(self.SERVER_ADDR)
		for action in self._get(url):
			self.actions[action['type']] = action['action_id']

	def upload_proposal(self, data: dict):
		data = {'action_id': self.actions['custom'], 'data': data}
		self._post(url=self.url, data=data)

	def upload_sample(self, data: dict):
		data = {'action_id': self.actions['sample'], 'data': data}
		self._post(url=self.url, data=data)

	def upload_dataset(self, data: dict):
		data = {'action_id': self.actions['measurement'], 'data': data}
		self._post(url=self.url, data=data)
