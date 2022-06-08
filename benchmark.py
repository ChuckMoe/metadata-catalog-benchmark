import datetime
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
from plotting import plot

DATA_DIR = Path('./volume/objects')


def load_data_file(filepath: Path) -> List[Dict]:
    with open(filepath, 'r') as handler:
        return json.load(handler)


def _test_schema_upload(
        connector: ConnectorInterface,
        schema: str,
        function: Callable,
        steps: int):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))

    data = load_data_file(
        DATA_DIR / connector.SUFFIX / '{}.json'.format(schema))
    logging.info('Data length: {}'.format(len(data)))
    logging.info('Step length: {}'.format(steps))

    return Timer(
        name=name,
        functions={'upload': function},
        data=data,
        steps=steps)


def _test_connector_upload(connector: ConnectorInterface, steps) -> List[
    Timer]:
    return [
        _test_schema_upload(
            connector,
            'proposals',
            connector.upload_proposals,
            steps),
        _test_schema_upload(
            connector,
            'samples',
            connector.upload_samples,
            steps),
        _test_schema_upload(
            connector,
            'datasets',
            connector.upload_datasets,
            steps),
        _test_schema_upload(
            connector,
            'datablocks',
            connector.upload_datablocks,
            steps)]


def test_connectors_upload(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_upload(connector, steps)
    return timers


def _test_schema_query(
        connector: ConnectorInterface,
        schema: str,
        functions: Dict[str, Callable]):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))
    return Timer(name=name, functions=functions)


def _test_connector_query(connector: ConnectorInterface) -> List[Timer]:
    functions = [
        {
            'query_zero': connector.query_zero_proposals,
            'query_one': connector.query_one_proposal,
            'query_some': connector.query_some_proposals,
            'query_all': connector.query_all_proposals
        },
        {
            'query_zero': connector.query_zero_samples,
            'query_one': connector.query_one_sample,
            'query_some': connector.query_some_samples,
            'query_all': connector.query_all_samples
        },
        {
            'query_zero': connector.query_zero_datasets,
            'query_one': connector.query_one_dataset,
            'query_some': connector.query_some_datasets,
            'query_all': connector.query_all_datasets
        },
        {
            'query_zero': connector.query_zero_datablocks,
            'query_one': connector.query_one_datablock,
            'query_some': connector.query_some_datablocks,
            'query_all': connector.query_all_datablocks
        }
    ]
    return [
        _test_schema_query(connector, 'proposals', functions[0]),
        _test_schema_query(connector, 'samples', functions[1]),
        _test_schema_query(connector, 'datasets', functions[2]),
        _test_schema_query(connector, 'datablocks', functions[3])
    ]


def test_connectors_queries():
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_query(connector)
    return timers


def _test_schema_all(
        connector: ConnectorInterface,
        schema: str,
        functions: Dict[str, Callable],
        steps: int):
    name = '{}.{}'.format(connector.SUFFIX, schema)
    logging.info('== {} =='.format(name))

    data = load_data_file(
        DATA_DIR / connector.SUFFIX / '{}.json'.format(schema))
    logging.info('Data length: {}'.format(len(data)))
    logging.info('Step length: {}'.format(steps))

    return Timer(name=name, functions=functions, data=data, steps=steps)


def _test_connector_all(connector: ConnectorInterface, steps) -> List[Timer]:
    functions = [
        {
            'upload': connector.upload_proposals,
            'query_zero': connector.query_zero_proposals,
            'query_one': connector.query_one_proposal,
            'query_some': connector.query_some_proposals,
            'query_all': connector.query_all_proposals
        },
        {
            'upload': connector.upload_samples,
            'query_zero': connector.query_zero_samples,
            'query_one': connector.query_one_sample,
            'query_some': connector.query_some_samples,
            'query_all': connector.query_all_samples
        },
        {
            'upload': connector.upload_datasets,
            'query_zero': connector.query_zero_datasets,
            'query_one': connector.query_one_dataset,
            'query_some': connector.query_some_datasets,
            'query_all': connector.query_all_datasets
        },
        {
            'upload': connector.upload_datablocks,
            'query_zero': connector.query_zero_datablocks,
            'query_one': connector.query_one_datablock,
            'query_some': connector.query_some_datablocks,
            'query_all': connector.query_all_datablocks
        }
    ]
    return [
        _test_schema_all(connector, 'proposals', functions[0], steps),
        _test_schema_all(connector, 'samples', functions[1], steps),
        _test_schema_all(connector, 'datasets', functions[2], steps),
        _test_schema_all(connector, 'datablocks', functions[3], steps)
    ]


def test_connectors_all(steps: int):
    timers: Dict[str, List[Timer]] = {}
    for connector in connectors:
        timers[connector.SUFFIX] = _test_connector_all(connector, steps)
    return timers


def init():
    log_filepath = 'logs/benchmark.{}.log'.format(datetime.datetime.now())
    logging.basicConfig(
        level=logging.INFO,
        encoding='utf-8',
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filepath, mode='a'),
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
    # Needed if DB is not empty. Otherwise, there will be conflicting object
    # IDs
    generate(5000)
    # test_connectors_upload(steps=100)
    # test_connectors_queries()
    test_connectors_all(steps=100)
    plot.create_plots_timing()
