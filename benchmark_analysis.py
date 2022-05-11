import csv
import datetime
import logging
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List


@dataclass
class Timer:
    name: str
    steps: int
    elapsed_time: List[float] = field(default=None, init=True, repr=True)
    elapsed_time_process: List[float] = field(default=None, init=True, repr=True)
    _start_time: List[float] = field(default=None, init=True, repr=False)
    _start_time_process: List[float] = field(default=None, init=True, repr=False)

    def __init__(self, name: str, function: Callable, data: List[Dict], steps: int):
        self.name = name
        self.len = len(data)
        self.steps = steps

        self._start_time = []
        self._start_time_process = []
        self.elapsed_time = []
        self.elapsed_time_process = []

        for i in range(math.ceil(self.len / steps) - 1):
            temp = data[i * steps: (i+1) * steps]

            self.__start()
            function(temp)
            self.__stop()

        self.export()

    def __start(self):
        """Start a new timer"""
        self._start_time.append(time.time())
        self._start_time_process.append(time.process_time())

    def __stop(self):
        """Stop the timer, and report the elapsed time"""
        # Calculate elapsed time
        self.elapsed_time.append(time.time() - self._start_time[-1])
        self.elapsed_time_process.append(time.process_time() - self._start_time_process[-1])

        # Report elapsed time
        logging.info('Elapsed time: {:0.4f} seconds'.format(self.elapsed_time[-1]))
        logging.info('Elapsed process time: {:0.4f} seconds'.format(self.elapsed_time_process[-1]))

    def export(self):
        dirpath = Path('./volume/timing/{}/{}'.format(self.len, self.steps))
        dirpath.mkdir(parents=True, exist_ok=True)

        filename = dirpath / '{}-{}.csv'.format(self.name, datetime.datetime.now())
        data = zip(self.elapsed_time, self.elapsed_time_process)

        with open(filename, 'w', newline='') as handler:
            cols = ['Elapsed Time', 'Elapsed CPU Time']
            writer = csv.writer(handler)
            writer.writerow(cols)

            for row in data:
                writer.writerow(row)
