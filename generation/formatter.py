import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from model.dataset import Dataset
from model.proposal import Proposal
from model.sample import Sample


class Formatter:
    DATA_FOLDER = Path('/home/mhannemann/Workspace/benchmark-metadata-catalog/volume/objects')
    SUFFIX: str

    def __init__(self):
        self.DATA_FOLDER = self.DATA_FOLDER / self.SUFFIX
        self.DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    def _format_text(self, value: str) -> str:
        return value

    def _format_bool(self, value: bool) -> bool:
        return value

    def _format_number(self, value: int) -> int:
        return value

    def _format_datetime(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def _format_list(self, values: List) -> List:
        return [self._format_data_by_type('', value) for value in values]

    def _format_object(self, obj) -> Dict:
        temp = {}
        for key, value in obj.__dict__.items():
            temp |= self._format_data_by_type(key, value)
        return temp

    def _format_data_by_type(self, key: str, value):
        if isinstance(value, str):
            data = self._format_text(value)
        elif isinstance(value, bool):
            data = self._format_bool(value)
        elif isinstance(value, int):
            data = self._format_number(value)
        elif isinstance(value, datetime):
            data = self._format_datetime(value)
        elif isinstance(value, list):
            data = self._format_list(value)
        else:
            data = self._format_object(value)

        if key == '':
            return data
        return {key: data}

    def format(self, objects: List) -> List[Dict]:
        return [self._format_object(obj) for obj in objects]

    def save_proposals(self, proposals: List[Proposal]):
        data = self.format(proposals)
        with open(self.DATA_FOLDER / 'proposals.json', 'w') as handler:
            json.dump(data, handler)

    def save_samples(self, samples: List[Sample]):
        data = self.format(samples)
        with open(self.DATA_FOLDER / 'samples.json', 'w') as handler:
            json.dump(data, handler)

    def save_datasets(self, datasets: List[Dataset]):
        data = self.format(datasets)
        with open(self.DATA_FOLDER / 'datasets.json', 'w') as handler:
            json.dump(data, handler)
