from dataclasses import dataclass, field
import time
from typing import Callable, List, Dict, Optional

from connectors.connector_interface import ConnectorInterface


class TimerError(Exception):
	"""A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer:
	name: str
	elapsed_time: Optional[float]
	elapsed_time_process: Optional[float]
	_start_time: Optional[float] = field(default=None, init=False, repr=False)
	_start_time_process: Optional[float] = field(default=None, init=False, repr=False)
	logger: Optional[Callable[[str], None]] = print

	def __init__(self, name: str):
		self.name = name

	def start(self) -> None:
		"""Start a new timer"""
		if self._start_time is not None:
			raise TimerError(f"Timer is already running")

		self._start_time = time.time()
		self._start_time_process = time.process_time()

	def stop(self) -> float:
		"""Stop the timer, and report the elapsed time"""
		if self._start_time is None:
			raise TimerError(f"Timer is not running. Use .start() to start it")

		# Calculate elapsed time
		self.elapsed_time = time.time() - self._start_time
		self.elapsed_time_process = time.process_time() - self._start_time_process

		# Report elapsed time
		if self.logger:
			self.logger('Elapsed time: {:0.4f} seconds'.format(self.elapsed_time))
			self.logger('Elapsed process time: {:0.4f} seconds'.format(self.elapsed_time_process))

		return self.elapsed_time


class Timers:
	__timers: Dict[str, Timer] = {}

	def __init__(self, connectors: List[ConnectorInterface]):
		for connector in connectors:
			self.__timers[str(connector)] = Timer(str(connector))

	def start(self, connector: ConnectorInterface):
		self.__timers[str(connector)].start()

	def stop(self, connector: ConnectorInterface):
		self.__timers[str(connector)].stop()

	def analyse(self):
		for name, timer in self.__timers.items():
			print(name, timer)
