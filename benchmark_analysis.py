import logging
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Timer:
	name: str
	elapsed_time: Optional[float]
	elapsed_time_process: Optional[float]
	_start_time: Optional[float] = field(default=None, init=False, repr=False)
	_start_time_process: Optional[float] = field(default=None, init=False, repr=False)

	def __init__(self, name: str):
		self.name = name

	def __enter__(self):
		"""Start a new timer"""
		self._start_time = time.time()
		self._start_time_process = time.process_time()

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Stop the timer, and report the elapsed time"""
		# Calculate elapsed time
		self.elapsed_time = time.time() - self._start_time
		self.elapsed_time_process = time.process_time() - self._start_time_process

		# Report elapsed time
		logging.info('Elapsed time: {:0.4f} seconds'.format(self.elapsed_time))
		logging.info('Elapsed process time: {:0.4f} seconds'.format(self.elapsed_time_process))

		return self.elapsed_time
