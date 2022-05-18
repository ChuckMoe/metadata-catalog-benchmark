import random
from typing import List

from generation.help import *


id_generator = infinite_id('Datablock')


class DataFile:
    path: str
    size: int
    time: datetime
    chk: str
    uid: str
    gid: str
    perm: str
    createdBy: str
    updatedBy: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self):
        self.path = generate_data_text()
        self.size = generate_data_number()
        self.time = generate_data_datetime()
        self.chk = generate_data_text()
        self.uid = generate_data_text()
        self.gid = generate_data_text()
        self.perm = generate_data_text()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()


class DataBlock:
    id: str
    size: int
    datasetId: str
    rawDatasetId: str
    derivedDatasetId: str
    dataFileList: List[DataFile]
    ownerGroup: str
    accessGroups: List[str]
    instrumentGroup: str
    createdBy: str
    updatedBy: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self, dataset_ids: List[str]):
        current_id = next(id_generator)
        dataset_id = 'PID/{}'.format(random.choice(dataset_ids))  # Scicat needs to associate valid ids for this
        self.datablockId = current_id
        self.size = int(current_id.split('/')[1])
        self.datasetId = dataset_id
        self.rawDatasetId = dataset_id
        self.derivedDatasetId = dataset_id
        self.dataFileList = [DataFile() for _ in range(randint(0, 20))]
        self.ownerGroup = generate_data_group()
        self.accessGroups = [generate_data_group()]
        self.instrumentGroup = generate_data_group()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()
