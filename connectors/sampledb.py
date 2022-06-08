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

    def __repr__(self):
        return 'SampleDB'

    def get_actions(self):
        url = '{}/actions'.format(self.SERVER_ADDR)
        for action in self._get(url):
            self.actions[action['type']] = action['action_id']

    def upload_proposal(self, data: dict):
        data = {'action_id': 1, 'data': data}
        self._post(url=self.url, data=data)

    def upload_sample(self, data: dict):
        data = {'action_id': self.actions['sample'], 'data': data}
        self._post(url=self.url, data=data)

    def upload_dataset(self, data: dict):
        data = {'action_id': self.actions['measurement'], 'data': data}
        self._post(url=self.url, data=data)

    def upload_datablock(self, data: dict):
        data = {'action_id': 4, 'data': data}
        self._post(url=self.url, data=data)

    def query_zero_proposals(self, **kwargs) -> List:
        query = {'action_id': 1, 'q': 'email == "investor"'}
        return self._get(url=self.url, params=query)

    def query_zero_samples(self, **kwargs) -> List:
        query = {'action_id': 2, 'q': 'sampleCharacteristics.metadata6 < 0 g'}
        return self._get(url=self.url, params=query)

    def query_zero_datasets(self, **kwargs) -> List:
        query = {'action_id': 3, 'q': 'principalInvestigator == "investor"'}
        return self._get(url=self.url, params=query)

    def query_zero_datablocks(self, **kwargs) -> List:
        query = {'action_id': 4, 'q': 'ownerGroup == "Group#99"'}
        return self._get(url=self.url, params=query)

    def query_one_proposal(self, **kwargs) -> List:
        query = {'action_id': 1, 'q': 'title == "Proposal/1"'}
        return self._get(url=self.url, params=query)

    def query_one_sample(self, **kwargs) -> List:
        query = {'action_id': 2, 'q': 'description == "Sample/1"'}
        return self._get(url=self.url, params=query)

    def query_one_dataset(self, **kwargs) -> List:
        query = {'action_id': 3, 'q': 'datasetName == "Dataset/1"'}
        return self._get(url=self.url, params=query)

    def query_one_datablock(self, **kwargs) -> List:
        query = {'action_id': 4, 'q': 'size == 0 g'}
        return self._get(url=self.url, params=query)

    def query_some_proposals(self, **kwargs) -> List:
        template = '(title == "Proposal/{}")'
        query = ' or '.join([template.format(i*100) for i in range(10)])
        query = {'action_id': 1, 'q': query}
        return self._get(url=self.url, params=query)

    def query_some_samples(self, **kwargs) -> List:
        query = {'action_id': 2, 'q': 'sampleCharacteristics.metadata6 < 15 g'}
        return self._get(url=self.url, params=query)

    def query_some_datasets(self, **kwargs) -> List:
        query = {'action_id': 3, 'q': 'size < 15 g'}
        return self._get(url=self.url, params=query)

    def query_some_datablocks(self, **kwargs) -> List:
        query = {'action_id': 4, 'q': 'size < 15 g'}
        return self._get(url=self.url, params=query)

    def query_all_proposals(self, **kwargs) -> List:
        query = {'action_id': 1, 'q': 'email == "api"'}
        return self._get(url=self.url, params=query)

    def query_all_samples(self, **kwargs) -> List:
        query = {'action_id': 2, 'q': 'sampleCharacteristics.metadata6 >= 0 g'}
        return self._get(url=self.url, params=query)

    def query_all_datasets(self, **kwargs) -> List:
        query = {'action_id': 3, 'q': 'principalInvestigator == "api"'}
        return self._get(url=self.url, params=query)

    def query_all_datablocks(self, **kwargs) -> List:
        query = {'action_id': 4, 'q': 'ownerGroup == "Group#1"'}
        return self._get(url=self.url, params=query)
