import uuid

from fastapi import HTTPException, status

from device_monitor.crud import BatteryRepository
from device_monitor.database.models import Battery


async def check_battery_exists(
    battery_id: uuid.UUID,
    repository: BatteryRepository,
) -> Battery:
    """Check if a battery exists in the database.

    Args:
        battery_id: Battery ID.
        repository: The repository used to access battery records.

    Raises:
        HTTPException: If the battery with the given identifier is not found,
            a 404 HTTPException is raised with an appropriate error message.

    Returns:
        The battery record if found.
    """
    battery = await repository.get_by_id(battery_id)
    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battery not found",
        )
    return battery
