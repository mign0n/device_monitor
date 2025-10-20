from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.database.models import Battery


class BatteryRepository:
    """Repository for managing battery data interactions with the database."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the BatteryRepository with a database session.

        Args:
            session: The asynchronous session for database operations.
        """
        self.session = session
        self.model = Battery

    async def get_all(self) -> Sequence[Battery]:
        """Retrieve all battery records from the database.

        Returns:
            A sequence containing all battery records.
        """
        async with self.session.begin():
            db_objs = await self.session.execute(select(self.model))
            return db_objs.scalars().all()
