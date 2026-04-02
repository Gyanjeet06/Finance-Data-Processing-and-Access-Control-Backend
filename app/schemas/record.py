from datetime import datetime
from typing import Literal

from pydantic import BaseModel

EntryType = Literal["income", "expense"]


class RecordBase(BaseModel):
    title: str
    amount: float
    entry_type: EntryType
    category: str | None = None
    notes: str | None = None


class RecordCreate(RecordBase):
    owner_id: int


class RecordUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    entry_type: EntryType | None = None
    category: str | None = None
    notes: str | None = None


class RecordRead(RecordBase):
    id: int
    date: datetime
    owner_id: int

    class Config:
        orm_mode = True
