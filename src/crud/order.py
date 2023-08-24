import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas

from .base import BaseCRUD


class OrderCRUD(BaseCRUD[models.Order, schemas.OrderCreate]):
    async def create(
        self,
        session: AsyncSession,
        *,
        object_in: schemas.OrderCreate
    ) -> models.Order:

        object_data = dict(object_in)
        order_items = object_data.pop('order_items')
        object_data['order_items'] = [
            models.OrderItem(
                item_id=order_item.item_id,
                amount=order_item.amount
            )
            for order_item in order_items
        ]

        return await self.add_commit_refresh(
            session,
            obj=models.Order(**object_data)
        )

    async def assign(
        self,
        session: AsyncSession,
        *,
        order: models.Order,
        courier: models.Courier
    ) -> models.Order:

        order.courier_id = courier.courier_id
        await session.refresh(courier)
        return await self.add_commit_refresh(session, obj=order)

    async def complete(
        self,
        session: AsyncSession,
        *,
        order: models.Order,
        completed_at: dt.datetime
    ) -> models.Order:

        order.completed_at = completed_at

        return await self.add_commit_refresh(session, obj=order)


order = OrderCRUD(models.Order)
