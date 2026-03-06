import re
from datetime import date as _date

from pydantic import BaseModel, field_validator


class Promise(BaseModel):
    promise: str
    source: str
    date: str

    @field_validator("date")
    @classmethod
    def ensure_date_format(cls, v: str) -> str:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            return v
        return _date.today().isoformat()
