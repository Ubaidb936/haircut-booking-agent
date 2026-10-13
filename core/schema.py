from pydantic import BaseModel
from typing import Optional

class Input(BaseModel):
    thread_id: str
    message: str


class Output(BaseModel):
    thread_id: str
    message: str
    customer_name: Optional[str] = None
    service_type: Optional[str] = None
    start_time: Optional[str] = None
    booked: bool = False


