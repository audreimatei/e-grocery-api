import datetime as dt

from src import models
from src.config import cfg


class CourierLogic:
    async def get_rating(
        self,
        courier: models.Courier,
        start_at: dt.datetime,
        end_at: dt.datetime
    ) -> float:

        if start_at == end_at:
            return 0

        completed_orders = [
            order
            for order in courier.orders
            if order.completed_at is not None
            and start_at.date() <= order.completed_at.date() < end_at.date()
        ]

        hours_diff = (
            (end_at - start_at).total_seconds() / cfg.SECONDS_IN_HOUR
        )

        rating_coeff = courier.courier_type.rating_coeff

        return round(len(completed_orders) / hours_diff * rating_coeff, 2)

    async def get_earnings(
        self,
        courier: models.Courier,
        start_at: dt.datetime,
        end_at: dt.datetime
    ) -> int:

        completion_orders_costs = [
            order.cost
            for order in courier.orders
            if order.completed_at is not None
            and start_at.date() <= order.completed_at.date() < end_at.date()
        ]

        return (
            len(completion_orders_costs)
            * sum(completion_orders_costs)
            * courier.courier_type.earnings_coeff
        )

    async def get_optimal_for_order(
        self,
        order: models.Order,
        couriers: list[models.Courier]
    ) -> models.Courier:

        return min(
            couriers,
            key=lambda courier: (courier.weight, len(courier.orders))
        )


courier = CourierLogic()
