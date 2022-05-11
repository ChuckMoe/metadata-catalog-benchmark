import json
import uuid
from datetime import datetime
from os import listdir
from pathlib import Path
from random import randint
from typing import Dict, List


class Generator:
	BASE_FOLDER = Path('/home/mhannemann/Workspace/benchmark-metadata-catalog/volume')
	SCHEMA_FOLDER = BASE_FOLDER / 'schemas'
	DATA_FOLDER = BASE_FOLDER / 'objects'
	SUFFIX: str

	TODAY = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def __init__(self, amount: int):
		for file in listdir(self.SCHEMA_FOLDER):
			if '.json' in file:
				self.current_filename = file
				with open(self.SCHEMA_FOLDER / file, 'r') as handler:
					current_schema = json.load(handler)
					data = [self.generate_data_object(schema=current_schema) for _ in range(amount)]

					with open(self.DATA_FOLDER / self.SUFFIX / file, 'w') as handler:
						json.dump(data, handler)

	def generate_data_text(self) -> str:
		return uuid.uuid4().__str__()

	def generate_data_datetime(self) -> str:
		return self.TODAY

	def generate_data_number(self) -> int:
		return randint(0, 99999)

	def generate_data_bool(self) -> bool:
		return True if randint(0, 1) == 1 else False

	def generate_data_array(self, schema: Dict, amount: int = None) -> List:
		schema = schema['items']
		if amount is None:
			amount = randint(0, 40)

		return [self.generate_data_by_type(schema['type'], schema) for _ in range(amount)]

	def generate_data_object(self, schema: Dict) -> Dict:
		schema = schema['properties']
		return {key: self.generate_data_by_type(schema[key]['type'], schema[key]) for key in schema.keys()}

	def generate_data_by_type(self, data_type: str, schema: Dict):
		if 'text' == data_type:
			return self.generate_data_text()
		elif 'bool' == data_type:
			return self.generate_data_bool()
		elif 'quantity' == data_type:
			return self.generate_data_number()
		elif 'datetime' == data_type:
			return self.generate_data_datetime()
		elif 'array' == data_type:
			return self.generate_data_array(schema)
		elif 'object' == data_type:
			return self.generate_data_object(schema)

