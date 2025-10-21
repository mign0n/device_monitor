from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.database.session import (
    sessionmaker,
)
from device_monitor.services import BatteryService, DeviceService


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Create and provide a database session for asynchronous operations.

    Yields:
        AsyncSession: An asynchronous database session.

    Raises:
        Exception: Propagates any exceptions that occur within the session
            operations.
    """
    async with sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_battery_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> BatteryService:
    """Retrieve the BatteryService instance with an active database session.

    Args:
        session: The active database session injected via dependency.

    Returns:
        An instance of the BatteryService for managing battery-related
        operations.
    """
    return BatteryService(session)


def get_device_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DeviceService:
    """Retrieve the DeviceService instance with an active database session.

    Args:
        session: The active database session injected via dependency.

    Returns:
        An instance of the DeviceService for managing battery-related
        operations.
    """
    return DeviceService(session)
