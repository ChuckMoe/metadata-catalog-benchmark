from typing import List

from generation.help import *


class SampleCharacteristics:
    metadata1: str
    metadata2: str
    metadata3: str
    metadata4: str
    metadata5: str
    metadata6: int
    metadata7: int
    metadata8: int
    metadata9: int
    metadata10: int
    metadata11: datetime
    metadata12: datetime

    def __init__(self):
        self.metadata1 = generate_data_text()
        self.metadata2 = generate_data_text()
        self.metadata2 = generate_data_text()
        self.metadata4 = generate_data_text()
        self.metadata5 = generate_data_text()
        self.metadata6 = generate_data_number()
        self.metadata7 = generate_data_number()
        self.metadata8 = generate_data_number()
        self.metadata9 = generate_data_number()
        self.metadata10 = generate_data_number()
        self.metadata11 = generate_data_datetime()
        self.metadata12 = generate_data_datetime()


class Sample:
    sampleId: str
    owner: str
    description: str
    sampleCharacteristics: SampleCharacteristics
    isPublished: bool
    ownerGroup: str
    accessGroups: List[str]
    instrumentGroup: str
    createdBy: str
    updatedBy: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self):
        self.sampleId = generate_data_text()
        self.owner = generate_data_user()
        self.description = generate_data_text()
        self.sampleCharacteristics = SampleCharacteristics()
        self.isPublished = generate_data_bool()
        self.ownerGroup = generate_data_group()
        self.accessGroups = [generate_data_group()]
        self.instrumentGroup = generate_data_group()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()
