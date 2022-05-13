import logging

from generation.sampledb import SampleDbFormatter
from generation.scicat import SciCatFormatter
from model.datablock import DataBlock
from model.dataset import Dataset
from model.proposal import Proposal
from model.sample import Sample


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

    def generate_proposals(self, amount: int = None):
        logging.info('Generate {} new Proposals'.format(amount))
        amount = self.default_amount if amount is None else amount
        data = [Proposal() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_proposals(proposals=data)

    def generate_samples(self, amount: int = None):
        logging.info('Generate {} new Samples'.format(amount))
        amount = self.default_amount if amount is None else amount
        data = [Sample() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_samples(data)

    def generate_datasets(self, amount: int = None):
        logging.info('Generate {} new Datasets'.format(amount))
        amount = self.default_amount if amount is None else amount
        data = [Dataset() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_datasets(data)

    def generate_datablocks(self, amount: int = None):
        logging.info('Generate {} new DataBlocks'.format(amount))
        amount = self.default_amount if amount is None else amount
        data = [DataBlock() for _ in range(amount)]
        for formatter in self.formatter:
            formatter.save_datablocks(data)


if __name__ == '__main__':
    g = Generator(amount=500)
    g.generate_datablocks()
