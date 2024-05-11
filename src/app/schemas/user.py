from pydantic import BaseModel
from schemas.student import StudentOut


class UserOut(BaseModel):
    student: StudentOut
    username: str
    is_active: bool
