from datetime import datetime

from pydantic import BaseModel
from schemas.address import AddressOut
from schemas.school import SchoolOut


class StudentOut(BaseModel):

    id: int
    firstname: str
    lastname: str
    school: SchoolOut
    address: AddressOut
    email: str
    driving_licence_nb: str
    driving_licence_validity: datetime


class StudentUpdate(BaseModel):

    firstname: str | None = None
    lastname: str | None = None
    school_id: int | None = None
    address_id: int | None = None
    email: str | None = None
    driving_licence_nb: str | None = None
    driving_licence_validity: datetime | None = None
