from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends

from device_monitor.database.models import Device
from device_monitor.dependencies import get_device_service
from device_monitor.schemas import DeviceDB
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
