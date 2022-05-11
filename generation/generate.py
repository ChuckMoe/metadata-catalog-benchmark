from generation.sampledb import SampleDbGenerator
from generation.scicat import SciCatGenerator

if __name__ == '__main__':
	amount_example_data: int = 1
	SampleDbGenerator(amount_example_data)
	SciCatGenerator(amount_example_data)
