import json
from pathlib import Path
from typing import Dict, List

from benchmark_analysis import Timers
from connectors.connector_interface import ConnectorInterface
from connectors.sampledb import SampleDB
from connectors.scicat import SciCat

DATA_DIR = Path('./volume/objects')


def load_data_file(filepath: Path) -> List[Dict]:
	with open(filepath, 'r') as handler:
		return json.load(handler)


def test_connector(connector: ConnectorInterface) -> None:
	connector.upload_proposals(load_data_file(DATA_DIR / connector.SUFFIX / 'proposal.action.json'))
	connector.upload_samples(load_data_file(DATA_DIR / connector.SUFFIX / 'sample.action.json'))
	connector.upload_datasets(load_data_file(DATA_DIR / connector.SUFFIX / 'measurement.action.json'))


def run():
	connectors = [
		SampleDB(),
		SciCat()
	]
	timers = Timers(connectors)
	for connector in connectors:
		timers.start(connector)
		test_connector(connector)
		timers.stop(connector)

	timers.analyse()


if __name__ == '__main__':
	run()
