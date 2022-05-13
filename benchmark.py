import json
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List

from benchmark_analysis import Timer
from connectors.connector_interface import ConnectorInterface
from connectors.sampledb import SampleDB
from connectors.scicat import SciCat

DATA_DIR = Path('./volume/objects')


def load_data_file(filepath: Path) -> List[Dict]:
    with open(filepath, 'r') as handler:
        return json.load(handler)


def _test_schema_upload(connector: ConnectorInterface, schema: str, function: Callable, steps: int):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))

    data = load_data_file(DATA_DIR / connector.SUFFIX / '{}.json'.format(schema))
    logging.info('Data length: {}'.format(len(data)))
    logging.info('Step length: {}'.format(steps))

    return Timer(name=name, function=function, data=data, steps=steps)


def _test_connector_upload(connector: ConnectorInterface, steps) -> List[Timer]:
    return [
        _test_schema_upload(connector, 'proposals.upload', connector.upload_proposals, steps),
        _test_schema_upload(connector, 'samples.upload', connector.upload_samples, steps),
        _test_schema_upload(connector, 'datasets.upload', connector.upload_datasets, steps)]


def test_connectors_upload(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_upload(connector, steps)
    return timers


def _test_schema_query(connector: ConnectorInterface, schema: str, function: Callable):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))
    return Timer(name=name, function=function)


def _test_connector_query(connector: ConnectorInterface) -> List[Timer]:
    return [
        _test_schema_query(connector, 'proposals.query', connector.query_proposals),
        _test_schema_query(connector, 'samples.query', connector.query_samples),
        _test_schema_query(connector, 'datasets.query', connector.query_datasets)]


def test_connectors_queries():
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_query(connector)
    return timers


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
    connectors = init()
    # generate(500)  # Needed if DB is not empty. Otherwise, there will be conflicting object IDs
    # test_connectors_upload(steps=100)
    test_connectors_queries()
