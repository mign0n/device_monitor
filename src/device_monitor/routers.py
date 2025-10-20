import uuid
from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends

from device_monitor.database.models import Battery
from device_monitor.dependencies import get_battery_service
from device_monitor.schemas import BatteryCreate, BatteryDB, BatteryUpdate
from device_monitor.services import BatteryService

router = APIRouter(tags=["Batteries"])


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
    "/battery",
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


@router.get(
    "/battery",
    response_model=BatteryDB,
    summary="Retrieve the battery by its ID.",
    description="This endpoint fetches the battery by ID from the database.",
)
async def get_battery(
    battery_id: uuid.UUID,
    battery_service: Annotated[BatteryService, Depends(get_battery_service)],
) -> Battery | None:
    """Retrieve the battery by its ID.

    Args:
        battery_id: Battery ID.
        battery_service: The service used to interact with battery records.

    Returns:
        Battery: The newly created battery record.
    """
    return await battery_service.get_by_id(battery_id)


@router.patch(
    "/battery",
    response_model=BatteryDB,
    summary="Update a battery data.",
    description=(
        "This endpoint updates an existing battery record in the database."
    ),
)
async def update_battery(
    battery_id: uuid.UUID,
    battery_data: BatteryUpdate,
    battery_service: Annotated[BatteryService, Depends(get_battery_service)],
) -> Battery | None:
    """Updates an existing battery record.

    Args:
        battery_id: The ID of the battery to update.
        battery_data: The data to update the battery record.
        battery_service: The service used to interact with battery records.

    Returns:
        Battery: The updated battery record.
    """
    return await battery_service.update(battery_id, battery_data)


@router.delete(
    "/battery",
    response_model=BatteryDB,
    summary="Delete the battery by its ID.",
    description="This endpoint removes the battery from the database.",
)
async def remove_battery(
    battery_id: uuid.UUID,
    battery_service: Annotated[BatteryService, Depends(get_battery_service)],
) -> Battery | None:
    """Remove the battery by its ID.

    Args:
        battery_id: Battery ID.
        battery_service: The service used to interact with battery records.

    Returns:
        The removed battery record.
    """
    return await battery_service.remove(battery_id)
