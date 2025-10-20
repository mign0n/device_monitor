import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.database.models import Battery
from device_monitor.schemas import BatteryCreate, BatteryUpdate


class BatteryRepository:
    """Repository for managing battery data interactions with the database."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the BatteryRepository with a database session.

        Args:
            session: The asynchronous session for database operations.
        """
        self.session = session
        self.model = Battery

    async def create(self, battery_data: BatteryCreate) -> Battery:
        """Create a battery record.

        Args:
            battery_data: The data to create a new battery record.

        Returns:
            A battery instance.
        """
        battery = Battery(**battery_data.model_dump())
        self.session.add(battery)
        await self.session.flush()
        await self.session.refresh(battery)
        return battery

    async def get_all(self) -> Sequence[Battery]:
        """Retrieve all battery records from the database.

        Returns:
            A sequence containing all battery records.
        """
        async with self.session.begin():
            db_objs = await self.session.execute(select(self.model))
            return db_objs.scalars().all()

    async def get_by_id(self, battery_id: uuid.UUID) -> Battery | None:
        """Create a battery record.

        Args:
            battery_id: Battery ID.

        Returns:
            A battery instance.
        """
        battery = await self.session.execute(
            select(self.model).where(self.model.id == battery_id)
        )
        return battery.scalar_one_or_none()

    async def update(
        self,
        battery_id: uuid.UUID,
        battery_data: BatteryUpdate,
    ) -> Battery | None:
        """Update a battery record.

        Args:
            battery_id: Battery ID.
            battery_data: The data to update a battery record.

        Returns:
            Updated battery instance.
        """
        battery = await self.get_by_id(battery_id)
        if not battery:
            return None
        for field, value in battery_data.model_dump(exclude_unset=True).items():
            setattr(battery, field, value)
        await self.session.flush()
        await self.session.refresh(battery)
        return battery
