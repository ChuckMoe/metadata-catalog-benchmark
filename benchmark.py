import json
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List

from benchmark_analysis import Timer
from connectors.connector_interface import ConnectorInterface
from connectors.sampledb import SampleDB
from connectors.scicat import SciCat
from generation.generator import generate

DATA_DIR = Path('./volume/objects')


def load_data_file(filepath: Path) -> List[Dict]:
    with open(filepath, 'r') as handler:
        return json.load(handler)


def test_schema(connector: ConnectorInterface, schema: str, function: Callable, steps: int):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))

    data = load_data_file(DATA_DIR / connector.SUFFIX / '{}.json'.format(schema))
    logging.info('Data length: {}'.format(len(data)))
    logging.info('Step length: {}'.format(steps))

    return Timer(name=name, function=function, data=data, steps=steps)


def test_connector_upload(connector: ConnectorInterface, steps) -> List[Timer]:
    return [
        test_schema(connector, 'proposals', connector.upload_proposals, steps),
        test_schema(connector, 'samples', connector.upload_samples, steps),
        test_schema(connector, 'datasets', connector.upload_datasets, steps)]


def test_connectors_upload(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = test_connector_upload(connector, steps)


def init():
    logging.basicConfig(
        level=logging.INFO,
        encoding='utf-8',
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler('logs/benchmark.log', mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info('=== New Benchmark Test ===')

    return [
        SampleDB(),
        SciCat()
    ]


if __name__ == '__main__':
    generate(30)
    connectors = init()
    test_connectors_upload(steps=50)
