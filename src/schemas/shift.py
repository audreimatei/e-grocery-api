import datetime as dt

from pydantic import UUID4

from .base import ORJSONModel


class ShiftBase(ORJSONModel):
    region_id: UUID4
    date: dt.date
    start_time: dt.time
    end_time: dt.time


class Shift(ShiftBase):
    shift_id: UUID4

    class Config:
        orm_mode = True


class ShiftCreate(ShiftBase):
    pass


class Shifts(ORJSONModel):
    shifts: list[Shift]


class ShiftsLimitOffset(Shifts):
    limit: int
    offset: int

    class Config:
        orm_mode = True
