from typing import Dict

from generation.generator import Generator


class SampleDbGenerator(Generator):
	SUFFIX = 'sampledb'

	def generate_data_text(self) -> Dict[str, str]:
		return {'_type': 'text', 'text': super().generate_data_text()}

	def generate_data_datetime(self) -> Dict[str, str]:
		return {'_type': 'datetime', 'utc_datetime': super().generate_data_datetime()}

	def generate_data_number(self) -> Dict[str, str]:
		return {
			'_type': 'quantity',
			'magnitude_in_base_units': super().generate_data_number(),
			'dimensionality': '[mass]',
			'units': 'g'}

	def generate_data_bool(self) -> Dict :
		return {'_type': 'bool', 'value': super().generate_data_bool()}
