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
