import json
import logging
from pathlib import Path
from typing import List

from generation.sampledb import SampleDbFormatter
from generation.scicat import SciCatFormatter
from model.datablock import DataBlock
from model.dataset import Dataset
from model.proposal import Proposal
from model.sample import Sample


def _load_existing_dataset_ids() -> List[str]:
    filepath_datasets = Path(__file__).parent.parent / 'volume/objects/scicat/datasets.json'
    with open(filepath_datasets, 'r') as handler:
        datasets = json.load(handler)
        return [dataset['pid'] for dataset in datasets]


def generate(amount: int):
    generator = Generator(amount=amount)
    generator.generate_proposals()
    generator.generate_samples()
    generator.generate_datasets()
    generator.generate_datablocks()


class Generator:
    def __init__(self, amount: int):
        self.default_amount = amount
        self.formatter = [SampleDbFormatter(), SciCatFormatter()]

    def generate_proposals(self, amount: int = None) -> List[Proposal]:
        amount = self.default_amount if amount is None else amount
        logging.info('Generate {} new Proposals'.format(amount))
        data = [Proposal() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_proposals(proposals=data)
        return data

    def generate_samples(self, amount: int = None) -> List[Sample]:
        amount = self.default_amount if amount is None else amount
        logging.info('Generate {} new Samples'.format(amount))
        data = [Sample() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_samples(data)
        return data

    def generate_datasets(self, amount: int = None) -> List[Dataset]:
        amount = self.default_amount if amount is None else amount
        logging.info('Generate {} new Datasets'.format(amount))
        data = [Dataset() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_datasets(data)
        return data

    def generate_datablocks(self, amount: int = None) -> List[DataBlock]:
        amount = self.default_amount if amount is None else amount
        logging.info('Generate {} new DataBlocks'.format(amount))
        dataset_ids = _load_existing_dataset_ids()
        data = [DataBlock(dataset_ids) for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_datablocks(data)
        return data


if __name__ == '__main__':
    generate(5)
