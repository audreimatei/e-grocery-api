import datetime as dt
from typing import Annotated

from fastapi import Depends, HTTPException, status

from src import models

from .base import GetByIdPathNameOr404


async def get_valid_shift_to_add(
    courier: Annotated[
        models.Courier,
        Depends(GetByIdPathNameOr404(models.Courier))
    ],
    shift: Annotated[models.Shift, Depends(GetByIdPathNameOr404(models.Shift))]
) -> models.Shift:

    utc_now = dt.datetime.utcnow()
    if (
        shift.date < utc_now.date()
        or shift.date == utc_now.date() and shift.end_time <= utc_now.time()

    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Shift with id={shift.shift_id} ended.'
        )

    if shift in courier.shifts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Shift with id={shift.shift_id} already added'
                f' to courier with id={courier.courier_id}.'
            )
        )

    return shift
