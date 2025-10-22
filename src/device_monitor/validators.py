import uuid
from typing import Any

from fastapi import HTTPException, status

from device_monitor.crud import BaseRepository, DeviceRepository, ModelType
from device_monitor.database.models import Device

MAX_BATTERIES_PER_DEVICE = 5


async def check_object_exists(
    obj_id: uuid.UUID,
    repository: BaseRepository[ModelType],
    detail: Any = "Object not found",
) -> ModelType:
    """Check if an object exists in the database.

    Args:
        obj_id: Object ID.
        repository: The repository used to access database object.
        detail: Any data to be sent to the client in the `detail` key of the
            JSON response.

    Raises:
        HTTPException: If the object with the given identifier is not found,
            a 404 HTTPException is raised with an appropriate error message.

    Returns:
        The Model object if found.
    """
    obj = await repository.get_by_id(obj_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
    return obj


async def check_device_name_duplicate(
    name: str,
    repository: DeviceRepository,
    detail: Any = (
        "A device with that name already exists. "
        "The device name must be unique."
    ),
) -> None:
    """Check if a device name is not unique.

    Args:
        name: Device name.
        repository: The repository used to access database object.
        detail: Any data to be sent to the client in the `detail` key of the
            JSON response.

    Raises:
        HTTPException: If a device with the given name exists in the database,
            a 400 HTTPException is raised with an appropriate error message.
    """
    if await repository.get_by_name(name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


def check_limit_batteries_per_device(
    device: Device,
    limitation: int = MAX_BATTERIES_PER_DEVICE,
    detail: Any = "No more than {} batteries can be connected to the device.",
) -> None:
    """Check maximum number of battery connections to the device.

    Args:
        device: Device.
        limitation: The maximum allowed number of batteries to connect.
        detail: Any data to be sent to the client in the `detail` key of the
            JSON response.

    Raises:
        HTTPException: If a device with the given name exists in the database,
            a 400 HTTPException is raised with an appropriate error message.
    """
    batteries_count = len(device.batteries)
    if batteries_count >= limitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail.format(limitation),
        )
