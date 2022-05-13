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
    len: int = None
    steps: int = None
    elapsed_time: List[float] = field(default=None, init=True, repr=True)
    elapsed_time_process: List[float] = field(default=None, init=True, repr=True)
    _start_time: List[float] = field(default=None, init=True, repr=False)
    _start_time_process: List[float] = field(default=None, init=True, repr=False)

    def __init__(self, name: str, function: Callable, data: List[Dict] = None, steps: int = None):
        self.name = name

        self._start_time = []
        self._start_time_process = []
        self.elapsed_time = []
        self.elapsed_time_process = []

        if data is None:
            self.__time_get(function)
        else:
            self.len = len(data)
            self.steps = steps
            self.__time_post(function, data, steps)

        self.export()

    def __time_post(self, function: Callable, data: List, steps):
        for i in range(math.ceil(self.len / steps) - 1):
            temp = data[i * steps: (i+1) * steps]

            self.__start()
            function(temp)
            self.__stop()

    def __time_get(self, function: Callable):
        self.__start()
        logging.info('Result length: {}'.format(len(function())))
        self.__stop()

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

    def _export_queries(self):
        dirpath = Path('./volume/timing/queries')
        dirpath.mkdir(parents=True, exist_ok=True)
        filename = dirpath / 'query.csv'
        data = zip([self.name], self.elapsed_time, self.elapsed_time_process)

        with open(filename, 'w', newline='') as handler:
            cols = ['Action', 'Elapsed Time', 'Elapsed CPU Time']
            writer = csv.writer(handler)
            writer.writerow(cols)

            for row in data:
                writer.writerow(row)

    def _export_posts(self):
        dirpath = Path('./volume/timing/{}/{}'.format(self.len, self.steps))
        dirpath.mkdir(parents=True, exist_ok=True)
        filename = dirpath / '{}.{}.csv'.format(self.name, datetime.datetime.now())
        data = zip(self.elapsed_time, self.elapsed_time_process)

        with open(filename, 'w', newline='') as handler:
            cols = ['Elapsed Time', 'Elapsed CPU Time']
            writer = csv.writer(handler)
            writer.writerow(cols)

            for row in data:
                writer.writerow(row)

    def export(self):
        if self.len is None:
            self._export_queries()
        else:
            self._export_posts()
