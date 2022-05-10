from typing import Dict

from generation.generator import Generator


class SciCatGenerator(Generator):
	SUFFIX = 'scicat'

	def generate_data_object(self, schema: Dict) -> Dict:
		data = {}
		schema = schema['properties']

		for key in schema.keys():
			new_key = key
			if 'name' == key:
				if 'proposal' in self.current_filename:
					new_key = 'proposalId'
				if 'sample' in self.current_filename:
					new_key = 'sampleId'
				if 'measurement' in self.current_filename:
					new_key = 'pid'

			data[new_key] = self.generate_data_by_type(schema[key]['type'], schema[key])

		return data
