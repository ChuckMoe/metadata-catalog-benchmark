import datetime
import json
import logging
import os
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


def test_schema(connector: ConnectorInterface, schema: str, function: Callable):
	name = '{}.{}'.format(connector.SUFFIX, schema)
	logging.info('== {} =='.format(name))

	data_file = load_data_file(DATA_DIR / connector.SUFFIX / '{}.action.json'.format(schema))
	logging.info('Data length: {}'.format(len(data_file)))

	with Timer(name=name) as timer:
		function(data=data_file)
		return timer


def test_connector(connector: ConnectorInterface) -> List[Timer]:
	return [
		test_schema(connector, 'proposal', connector.upload_proposals),
		test_schema(connector, 'sample', connector.upload_samples),
		test_schema(connector, 'measurement', connector.upload_datasets)]


def test_connectors():
	logging.basicConfig(
		level=logging.INFO,
		encoding='utf-8',
		format="%(asctime)s [%(levelname)s] %(message)s",
		handlers=[
			logging.FileHandler('./logs/benchmark.txt', mode='a'),
			logging.StreamHandler(sys.stdout)
		]
	)
	logging.info('=== New Benchmark Test ===')

	connectors = [
		SampleDB(),
		SciCat()
	]

	timers: Dict[str, List[Timer]] = {}
	for connector in connectors:
		timers[connector.SUFFIX] = test_connector(connector)


if __name__ == '__main__':
	test_connectors()
