import csv
import datetime
import logging
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List


@dataclass
class Timer:
    name: str
    len: int
    steps: int
    elapsed_time: List[Dict] = field(default=None, init=True, repr=True)
    _current_timing: Dict[str, Any] = field(default=None, init=True, repr=False)
    # {offset, steps, start_time, function1_elapsed_time, functionX_elapsed_time, ...}

    def __init__(self, name: str, functions: Dict[str, Callable], data: List = None, steps: int = 1):
        if data is None:
            data = []

        self.name = name
        self.len = len(data)
        self.steps = steps

        self._current_timing = {'Offset': 0, 'Steps': steps}
        self.elapsed_time = []

        self.__time_functions(functions, data)
        self.export()

    def __time_function(self, func_name: str, function: Callable, data: List):
        self.__start_function()
        response = function(data=data)
        self.__stop_function(func_name)
        if 'query' in func_name:
            logging.info('Result length: {}'.format(len(response)))

    def __time_functions(self, functions: Dict[str, Callable], data: List):
        _range = 1 if len(data) == 0 else math.ceil(self.len / self.steps)
        for i in range(_range):
            temp = data[i * self.steps: (i + 1) * self.steps]

            self.__start(offset=i)
            for func_name, function in functions.items():
                self.__time_function(func_name, function, temp)
            self.__stop()

    def __start_function(self):
        """Start a new timer"""
        self._current_timing['start_time'] = time.time()

    def __stop_function(self, func_name: str):
        """Stop the timer, and report the elapsed time"""
        key = '{} - Elapsed Time'.format(func_name)
        self._current_timing[key] = time.time() - self._current_timing['start_time']
        logging.info('{} - Elapsed time: {:0.4f} seconds'.format(func_name, self._current_timing[key]))

    def __start(self, offset):
        self._current_timing = {'Offset': offset, 'Steps': self.steps}

    def __stop(self):
        self.elapsed_time.append(self._current_timing)

    def export(self):
        if 0 == self.len:
            dirpath = Path('./output/timing/queries')
        else:
            dirpath = Path('./output/timing/{}/{}'.format(self.len, self.steps))
        dirpath.mkdir(parents=True, exist_ok=True)
        filename = dirpath / '{}.{}.csv'.format(self.name, datetime.datetime.now())

        with open(filename, 'w', newline='') as handler:
            cols = self.elapsed_time[0].keys()
            writer = csv.DictWriter(handler, fieldnames=cols)
            writer.writeheader()
            writer.writerows(self.elapsed_time)
