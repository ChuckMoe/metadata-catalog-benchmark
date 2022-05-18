from typing import List

from generation.help import *


id_generator = infinite_id('Dataset')


class Technique:
    pid: str
    name: str

    def __init__(self):
        self.pid = generate_data_text()
        self.name = generate_data_text()


class DatasetLifecycle:
    # id: str
    archivable: bool
    retrievable: bool
    publishable: bool
    dateOfDiskPurging: datetime
    archiveRetentionTime: datetime
    dateOfPublishing: datetime
    publishedOn: datetime
    isOnCentralDisk: bool
    archiveStatusMessage: str
    retrieveStatusMessage: str
    archiveReturnMessage: str
    retrieveReturnMessage: str
    exportedTo: str
    retrieveIntegrityCheck: bool

    def __init__(self):
        # self.id = generate_data_text()
        self.archivable = generate_data_bool()
        self.retrievable = True
        self.publishable = generate_data_bool()
        self.dateOfDiskPurging = datetime.strptime('2999-12-31 12:00:00', '%Y-%m-%d %H:%M:%S')
        self.archiveRetentionTime = self.dateOfDiskPurging
        self.dateOfPublishing = generate_data_datetime()
        self.publishedOn = generate_data_datetime()
        self.isOnCentralDisk = generate_data_bool()
        self.archiveStatusMessage = generate_data_text()
        self.retrieveStatusMessage = generate_data_text()
        self.archiveReturnMessage = generate_data_text()
        self.retrieveReturnMessage = generate_data_text()
        self.exportedTo: generate_data_text()
        self.retrieveIntegrityCheck: generate_data_bool()


class ScientificMetadata:
    archivable: bool
    retrievable: bool
    publishable: bool

    def __init__(self):
        self.archivable = generate_data_bool()
        self.retrievable = generate_data_bool()
        self.publishable = generate_data_bool()


class Dataset:
    pid: str
    datasetName: str
    owner: str
    ownerEmail: str
    principalInvestigator: str
    contactEmail: str
    creationLocation: str
    sampleId: str
    proposalId: str
    instrumentId: str
    description: str
    dataFormat: str
    sourceFolder: str
    sourceFolderHost: str
    size: int
    packedSize: int
    numberOfFiles: int
    numberOfFilesArchived: int
    type: str
    validationStatus: str
    classification: str
    license: str
    version: str
    dataQualityMetrics: int
    comments: str
    isPublished: bool
    keywords: List[str]
    sharedWith: List[str]
    history: List[str]
    techniques: List[Technique]
    scientificMetadata: ScientificMetadata
    datasetLifecycle: DatasetLifecycle
    creationTime: datetime
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
        self.pid = current_id
        self.datasetName = current_id
        self.owner = generate_data_user()
        self.ownerEmail = generate_data_user()
        self.principalInvestigator = generate_data_user()
        self.contactEmail = generate_data_user()
        self.creationLocation = generate_data_text()
        self.sampleId = generate_data_text()
        self.proposalId = generate_data_text()
        self.instrumentId = generate_data_text()
        self.description = generate_data_text()
        self.dataFormat = generate_data_text()
        self.sourceFolder = generate_data_text()
        self.sourceFolderHost = generate_data_text()
        self.size = generate_data_number()
        self.packedSize = generate_data_number()
        self.numberOfFiles = generate_data_number()
        self.numberOfFilesArchived = generate_data_number()
        self.type = 'Raw'
        self.validationStatus = "valid"
        self.classification = generate_data_text()
        self.license = 'GNU'
        self.version = '1'
        self.dataQualityMetrics = generate_data_number()
        self.comments = generate_data_text()
        self.isPublished = generate_data_bool()
        self.keywords = [generate_data_text() for _ in range(randint(0, 10))]
        self.sharedWith = [generate_data_user()]
        self.history = [generate_data_text() for _ in range(randint(0, 20))]
        self.techniques = [Technique() for _ in range(randint(0, 5))]
        self.scientificMetadata = ScientificMetadata()
        self.datasetLifecycle = DatasetLifecycle()
        self.creationTime = generate_data_datetime()
        self.endTime = generate_data_datetime()
        self.ownerGroup = generate_data_group()
        self.accessGroups = [generate_data_group()]
        self.instrumentGroup = generate_data_group()
        self.createdBy = generate_data_user()
        self.updatedBy = generate_data_user()
        self.createdAt = generate_data_datetime()
        self.updatedAt = generate_data_datetime()
