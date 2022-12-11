import random
import string
from dataclasses import dataclass
from datetime import datetime

from configs import Formats


@dataclass(init=True)
class Student:
    firstName: str
    lastName: str
    collegeId: str
    collegeEmailId: str
    dateOfBirth: str
    phoneNumber: str
    hostelName: str
    imageUrl: str = "null"
    password: str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(4))
    studentId: str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    updatedTimestamp: str = datetime.now().strftime(Formats.timestamp_format)
    createdTimestamp: str = datetime.now().strftime(Formats.timestamp_format)


@dataclass(init=True)
class Security:
    firstName: str
    lastName: str
    emailId: str
    dateOfBirth: str
    phoneNumber: str
    designation: str
    securityId: str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    updatedTimestamp: str = datetime.now().strftime(Formats.timestamp_format)
    createdTimestamp: str = datetime.now().strftime(Formats.timestamp_format)


@dataclass(init=True)
class Building:
    buildingId: str
    buildType: str


@dataclass(init=True)
class EntryRequest:
    securityId: str
    studentId: str
    buildingId: str
    entryId: str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    updatedTimestamp: str = datetime.now().strftime(Formats.timestamp_format)
    createdTimestamp: str = datetime.now().strftime(Formats.timestamp_format)


@dataclass(init=True)
class EntryResponse:
    securityId: str
    studentId: str
    instituteId: str
    studentInfo: dict
    entryId: str = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    updatedTimestamp: str = datetime.now().strftime(Formats.timestamp_format)
    createdTimestamp: str = datetime.now().strftime(Formats.timestamp_format)
