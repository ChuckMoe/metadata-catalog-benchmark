from typing import List

from connectors.connector_interface import ConnectorInterface

PORT = 3000
SERVER_ADDR = 'http://localhost:{}/api/v3'.format(PORT)
USERNAME = 'ingestor'
PASSWORD = 'aman'


class SciCat(ConnectorInterface):
    SUFFIX = 'scicat'

    def __repr__(self):
        return "SciCat"

    def _authenticate(self):
        url = '{}/Users/login'.format(SERVER_ADDR)
        data = {'username': USERNAME, 'password': PASSWORD}
        self.API_KEY = self._post(url=url, data=data)['id']

    def upload_proposal(self, data: dict):
        url = '{}/Proposals'.format(SERVER_ADDR)
        self._post(url=url, data=data)

    def upload_sample(self, data: dict):
        url = '{}/Samples'.format(SERVER_ADDR)
        self._post(url=url, data=data)

    def upload_dataset(self, data: dict):
        url = '{}/RawDatasets'.format(SERVER_ADDR)
        self._post(url=url, data=data)

    def upload_datablock(self, data: dict):
        url = '{}/OrigDatablocks'.format(SERVER_ADDR)
        self._post(url=url, data=data)

    def query_proposals(self, **kwargs) -> List:
        url = '{}/Proposals'.format(SERVER_ADDR)
        query = {'filter[where][email][eq]': 'api'}
        return self._get(url=url, params=query)

    def query_samples(self, **kwargs) -> List:
        url = '{}/Samples'.format(SERVER_ADDR)
        # filter[where][nested.attribute] not working
        query = {'filter': '{"where": {"sampleCharacteristics.metadata6": {"gte": 0}}}'}
        return self._get(url=url, params=query)

    def query_datasets(self, **kwargs) -> List:
        url = '{}/RawDatasets'.format(SERVER_ADDR)
        query = {'filter[where][principalInvestigator][eq]': 'api'}
        return self._get(url=url, params=query)

    def query_datablocks(self, **kwargs) -> List:
        url = '{}/OrigDatablocks'.format(SERVER_ADDR)
        query = {'filter[where][ownerGroup][eq]': 'Group#1'}
        return self._get(url=url, params=query)
