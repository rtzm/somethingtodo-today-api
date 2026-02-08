from datetime import date, datetime
from pydantic import BaseModel


class Prompt(BaseModel):
    # TODO: convert to UUID
    id: int
    text: str
    use_date: date
    created_timestamp: datetime
    updated_timestamp: datetime
