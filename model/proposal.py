from typing import List

from generation.help import *


id_generator = infinite_id('Proposal')


class MeasurementPeriod:
    id: str
    instrument: str
    comment: str
    start: datetime
    end: datetime
    createdBy: str
    updatedBy: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self):
        self.id = generate_data_text()
        self.instrument = generate_data_text()
        self.comment = generate_data_text()
        self.start = generate_data_datetime()
        self.end = generate_data_datetime()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()


class Proposal:
    proposalId: str
    pi_email: str
    pi_firstname: str
    pi_lastname: str
    email: str
    firstname: str
    lastname: str
    title: str
    abstract: str
    MeasurementPeriodList: List[MeasurementPeriod]
    startTime: datetime
    endTime: datetime
    ownerGroup: str
    accessGroups: List[str]
    instrumentGroup: str
    createdBy: str
    updatedBy: str
    createdAt: datetime
    updatedAt: datetime

    def __init__(self):
        current_id = next(id_generator)
        self.proposalId = current_id
        self.pi_email = generate_data_text()
        self.pi_firstname = generate_data_user()
        self.pi_lastname = generate_data_user()
        self.email = generate_data_user()
        self.firstname = generate_data_user()
        self.lastname = generate_data_user()
        self.title = current_id
        self.abstract = generate_data_text()
        self.MeasurementPeriodList = [MeasurementPeriod() for _ in range(randint(0, 20))]
        self.startTime = generate_data_datetime()
        self.endTime = generate_data_datetime()
        self.ownerGroup = generate_data_group()
        self.accessGroups = [generate_data_group()]
        self.instrumentGroup = generate_data_group()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()
