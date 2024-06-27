from datetime import datetime

from pydantic import BaseModel
from schemas.student import StudentOut


class MessageOut(BaseModel):
    id: int
    sender: StudentOut
    recipient: StudentOut
    message: str
    created_at: datetime
