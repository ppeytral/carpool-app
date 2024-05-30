from pydantic import BaseModel
from schemas.student import StudentOut


class UserOut(BaseModel):
    id: int
    student: StudentOut
    username: str
    is_active: bool
