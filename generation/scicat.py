from generation.formatter import Formatter


class SciCatFormatter(Formatter):
    SUFFIX = 'scicat'

    def _format_data_by_type(self, key: str, value):
        data = super(SciCatFormatter, self)._format_data_by_type(key, value)

        if 'datablockId' == key:
            return {'id': data[key]}
        return data
