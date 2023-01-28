import datetime

from pydantic import BaseModel, validator
from typing import List


class ProgramBase(BaseModel):
    title: str
    url: str
    category: str
    organization: str
    subject: str
    apply_period: str
    apply_method: str
    content: str
    inquiries: str
    age: str

    class Config:
        orm_mode = True
