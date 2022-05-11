import datetime
from typing import Dict

from generation.formatter import Formatter


class SampleDbFormatter(Formatter):
    SUFFIX = 'sampledb'

    def _format_text(self, value: str) -> Dict[str, str]:
        return {'_type': 'text', 'text': value}

    def _format_bool(self, value: bool) -> Dict[str, bool]:
        return {'_type': 'bool', 'value': value}

    def _format_number(self, value: int) -> Dict[str, int]:
        return {
            '_type': 'quantity',
            'magnitude_in_base_units': value,
            'dimensionality': '[mass]',
            'units': 'g'}

    def _format_datetime(self, value: datetime.datetime) -> Dict[str, str]:
        return {'_type': 'datetime', 'utc_datetime': value.strftime('%Y-%m-%d %H:%M:%S')}

    def _format_data_by_type(self, key: str, value):
        data = super(SampleDbFormatter, self)._format_data_by_type(key, value)

        # SampleDB needs a 'name' attribute
        if key in ['proposalId', 'sampleId', 'pid']:
            return {'name': data[key]}
        return data
