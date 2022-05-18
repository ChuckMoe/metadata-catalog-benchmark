import uuid
from datetime import datetime
from random import randint
from typing import Generator

NOW: datetime = datetime.now()


def infinite_id(prefix: str) -> Generator[str, str, None]:
    num = 0
    while True:
        yield '{}/{}'.format(prefix, num)
        num += 1


def generate_data_user() -> str:
    return 'api'


def generate_data_group() -> str:
    return 'Group#1'


def generate_data_text() -> str:
    return uuid.uuid4().__str__()


def generate_data_datetime() -> datetime:
    return NOW


def generate_data_number() -> int:
    return randint(1, 100)


def generate_data_bool() -> bool:
    return True if randint(0, 1) == 1 else False
