from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends

from device_monitor.database.models import Battery
from device_monitor.dependencies import get_battery_service
from device_monitor.schemas import BatteryCreate, BatteryDB
from device_monitor.services import BatteryService

router = APIRouter()


@router.get(
    "/batteries",
    response_model=list[BatteryDB],
    summary="Retrieve a list of all batteries.",
    description="This endpoint fetches all battery records from the database.",
)
async def get_batteries(
    battery_service: Annotated[BatteryService, Depends(get_battery_service)],
) -> Sequence[Battery]:
    """Retrieve a list of all batteries.

    Args:
        battery_service: The service used to interact with battery records.

    Returns:
        A sequence containing all battery records.
    """
    return await battery_service.get_all()


@router.post(
    "/batteries",
    response_model=BatteryDB,
    summary="Create a battery.",
    description="This endpoint creates new battery record in the database.",
)
async def create_battery(
    battery_data: BatteryCreate,
    battery_service: Annotated[BatteryService, Depends(get_battery_service)],
) -> Battery:
    """Create a new battery record.

    Args:
        battery_data: The data to create a new battery record.
        battery_service: The service used to interact with battery records.

    Returns:
        Battery: The newly created battery record.
    """
    return await battery_service.create(battery_data)
