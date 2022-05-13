from typing import List

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
        print(self.actions)

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

    def upload_datablock(self, data: dict):
        data = {'action_id': self.actions[''], 'data': data}  # Todo
        self._post(url=self.url, data=data)

    def query_proposals(self) -> List:
        query = {'q': 'action={}&pi_email != "api"'.format(self.actions['custom'])}
        return self._get(url=self.url, params=query)

    def query_samples(self) -> List:
        query = {'q': 'action={}&sampleCharacteristics.metadata6 > 40000 g'.format(self.actions['sample'])}
        return self._get(url=self.url, params=query)

    def query_datasets(self) -> List:
        query = {'q': 'action={}&scientificMetadata.publishable == true'.format(self.actions['measurement'])}
        return self._get(url=self.url, params=query)

    def query_datablocks(self) -> List:
        query = {'q': 'action={}&dataFileList.path != abcd'.format(self.actions[''])}  # Todo
        return self._get(url=self.url, params=query)
