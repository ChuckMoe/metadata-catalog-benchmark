from typing import List

from generation.help import *


class DataFile:
    path: str
    size: int
    time: datetime
    chk: str
    uid: str
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
        self.perm = generate_data_text()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()


class DataBlock:
    id: str
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

    def __init__(self):
        self.id = generate_data_text()
        self.datasetId = generate_data_text()
        self.rawDatasetId = generate_data_text()
        self.derivedDatasetId = generate_data_text()
        self.dataFileList = [DataFile() for _ in range(randint(0, 20))]
        self.ownerGroup = generate_data_group()
        self.accessGroups = [generate_data_group()]
        self.instrumentGroup = generate_data_group()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()
