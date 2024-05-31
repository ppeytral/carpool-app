from datetime import datetime

from pydantic import BaseModel
from schemas.student import StudentOut


class UserUpdate(BaseModel):
    student_id: int | None = None
    password: str | None = None
    is_active: bool | None = None
    username: str | None = None
    updated_at: datetime = datetime.now()


class UserOut(BaseModel):
    id: int
    student: StudentOut
    username: str
    is_active: bool
    is_admin: bool
    is_moderator: bool
    created_at: datetime
    updated_at: datetime
