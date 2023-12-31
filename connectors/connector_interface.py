import logging
from typing import List

import requests


class ConnectorInterface:
    SUFFIX: str
    PORT: int
    SERVER_ADDR: str
    USERNAME: str
    PASSWORD: str
    API_KEY: str = None

    def __init__(self):
        logging.info('Creating connector {}'.format(self.SUFFIX))
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

    def upload_datablock(self, data: dict):
        """ Upload a single datablock """
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

    def upload_datablocks(self, data: list):
        """ Upload multiple datablocks """
        for entry in data:
            self.upload_datablock(entry)

    def query_zero_proposals(self, **kwargs) -> List:
        """ query zero proposals """

    def query_zero_samples(self, **kwargs) -> List:
        """ query zero samples """

    def query_zero_datasets(self, **kwargs) -> List:
        """ query zero raw_datasets/measurements """

    def query_zero_datablocks(self, **kwargs) -> List:
        """ query zero datablocks """

    def query_one_proposal(self, **kwargs) -> List:
        """ query zero proposal """

    def query_one_sample(self, **kwargs) -> List:
        """ query one sample """

    def query_one_dataset(self, **kwargs) -> List:
        """ query one raw_dataset/measurement """

    def query_one_datablock(self, **kwargs) -> List:
        """ query one datablock """

    def query_some_proposals(self, **kwargs) -> List:
        """ query multiple proposals """

    def query_some_samples(self, **kwargs) -> List:
        """ query multiple samples """

    def query_some_datasets(self, **kwargs) -> List:
        """ query multiple raw_datasets/measurements """

    def query_some_datablocks(self, **kwargs) -> List:
        """ query multiple datablocks """

    def query_all_proposals(self, **kwargs) -> List:
        """ query multiple proposals """

    def query_all_samples(self, **kwargs) -> List:
        """ query multiple samples """

    def query_all_datasets(self, **kwargs) -> List:
        """ query multiple raw_datasets/measurements """

    def query_all_datablocks(self, **kwargs) -> List:
        """ query multiple datablocks """
