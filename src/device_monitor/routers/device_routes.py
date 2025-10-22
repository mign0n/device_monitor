import uuid
from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends

from device_monitor.database.models import Device
from device_monitor.dependencies import get_device_service
from device_monitor.schemas import DeviceCreate, DeviceDB
from device_monitor.services import DeviceService

device_router = APIRouter(tags=["Devices"])


@device_router.get(
    "/devices",
    response_model=list[DeviceDB],
    summary="Retrieve a list of all devices.",
    description="This endpoint fetches all device records from the database.",
)
async def get_devices(
    device_service: Annotated[DeviceService, Depends(get_device_service)],
) -> Sequence[Device]:
    """Retrieve a list of all devices.

    Args:
        device_service: The service used to interact with device records.

    Returns:
        A sequence containing all device records.
    """
    return await device_service.get_all()


@device_router.post(
    "/device",
    response_model=DeviceDB,
    summary="Create a device.",
    description="This endpoint creates new device record in the database.",
)
async def create_device(
    device_data: DeviceCreate,
    device_service: Annotated[DeviceService, Depends(get_device_service)],
) -> Device:
    """Create a new device record.

    Args:
        device_data: The data to create a new device record.
        device_service: The service used to interact with device records.

    Returns:
        The newly created device record.
    """
    return await device_service.create(device_data)


@device_router.get(
    "/device",
    response_model=DeviceDB,
    summary="Retrieve the device by its ID.",
    description="This endpoint fetches the device by ID from the database.",
)
async def get_device(
    device_id: uuid.UUID,
    device_service: Annotated[DeviceService, Depends(get_device_service)],
) -> Device | None:
    """Retrieve the device by its ID.

    Args:
        device_id: Device ID.
        device_service: The service used to interact with device records.

    Returns:
        The newly created device record.
    """
    return await device_service.get_by_id(device_id)
