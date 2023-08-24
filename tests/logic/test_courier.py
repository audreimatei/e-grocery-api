from src import logic, models
from src.config import cfg_test


async def test_get_rating(
    db_courier_with_completed_orders: models.Courier
) -> None:

    rating = await logic.courier.get_rating(
        courier=db_courier_with_completed_orders,
        start_at=cfg_test.COURIER_START_AT,
        end_at=cfg_test.COURIER_END_AT
    )
    assert rating == cfg_test.COURIER_RATING


async def test_get_earnings(
    db_courier_with_completed_orders: models.Courier
) -> None:

    earnings = await logic.courier.get_earnings(
        courier=db_courier_with_completed_orders,
        start_at=cfg_test.COURIER_START_AT,
        end_at=cfg_test.COURIER_END_AT
    )
    assert earnings == cfg_test.COURIER_EARNINGS
