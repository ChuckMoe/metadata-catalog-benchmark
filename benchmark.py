import datetime
import json
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List

from plotting import plot
from benchmark_analysis import Timer
from connectors.connector_interface import ConnectorInterface
from connectors.sampledb import SampleDB
from connectors.scicat import SciCat
from generation.generator import generate

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

    return Timer(name=name, functions={'upload': function}, data=data, steps=steps)


def _test_connector_upload(connector: ConnectorInterface, steps) -> List[Timer]:
    return [
        _test_schema_upload(connector, 'proposals', connector.upload_proposals, steps),
        _test_schema_upload(connector, 'samples', connector.upload_samples, steps),
        _test_schema_upload(connector, 'datasets', connector.upload_datasets, steps),
        _test_schema_upload(connector, 'datablocks', connector.upload_datablocks, steps)]


def test_connectors_upload(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_upload(connector, steps)
    return timers


def _test_schema_query(connector: ConnectorInterface, schema: str, function: Callable):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))
    return Timer(name=name, functions={'query': function})


def _test_connector_query(connector: ConnectorInterface) -> List[Timer]:
    return [
        _test_schema_query(connector, 'proposals', connector.query_proposals),
        _test_schema_query(connector, 'samples', connector.query_samples),
        _test_schema_query(connector, 'datasets', connector.query_datasets),
        _test_schema_query(connector, 'datablocks', connector.query_datablocks)]


def test_connectors_queries():
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_query(connector)
    return timers


def _test_schema_all(connector: ConnectorInterface, schema: str, functions: Dict[str, Callable], steps: int):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))

    data = load_data_file(DATA_DIR / connector.SUFFIX / '{}.json'.format(schema))
    logging.info('Data length: {}'.format(len(data)))
    logging.info('Step length: {}'.format(steps))

    return Timer(name=name, functions=functions, data=data, steps=steps)


def _test_connector_all(connector: ConnectorInterface, steps) -> List[Timer]:
    functions = [
        {'upload': connector.upload_proposals, 'query': connector.query_proposals},
        {'upload': connector.upload_samples, 'query': connector.query_samples},
        {'upload': connector.upload_datasets, 'query': connector.query_datasets},
        {'upload': connector.upload_datablocks, 'query': connector.query_datablocks}
    ]
    return [
        _test_schema_all(connector, 'proposals', functions[0], steps),
        _test_schema_all(connector, 'samples', functions[1], steps),
        _test_schema_all(connector, 'datasets', functions[2], steps),
        _test_schema_all(connector, 'datablocks', functions[3], steps)]


def test_connectors_all(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_all(connector, steps)
    return timers


def init():
    logging.basicConfig(
        level=logging.INFO,
        encoding='utf-8',
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler('logs/benchmark.{}.log'.format(datetime.datetime.now()), mode='a'),
            # logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info('=== New Benchmark Test ===')

    return [
        SampleDB(),
        SciCat()
    ]


if __name__ == '__main__':
    connectors = init()
    # generate(200)  # Needed if DB is not empty. Otherwise, there will be conflicting object IDs
    # test_connectors_upload(steps=100)
    # test_connectors_queries()
    test_connectors_all(steps=100)
    plot.create_plots_timing()
