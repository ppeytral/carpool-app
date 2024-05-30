from typing import Optional

from pydantic import BaseModel
from schemas.student import StudentOut


class UserUpdate(BaseModel):
    student_id: int | None = None
    password: str | None = None
    is_active: bool | None = None
    username: str | None = None


class UserOut(BaseModel):
    id: int
    student: StudentOut
    username: str
    is_active: bool
