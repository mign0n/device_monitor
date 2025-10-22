import uuid
from collections.abc import Sequence
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.database.base import Base
from device_monitor.database.models import Battery, Device

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository[ModelType: Base]:
    """Base repository for managing data interactions with the database."""

    model: type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        """Init the repository using a database session and a specific model.

        Args:
            session: The asynchronous session for database operations.
            model: Database model.
        """
        self.session = session

    async def create(self, data: BaseModel) -> ModelType:
        """Create a new record corresponding to a specific model.

        Args:
            data: The data to create a new record.

        Returns:
            Created object of a specific model.
        """
        data_obj = self.model(**data.model_dump())
        self.session.add(data_obj)
        await self.session.flush()
        await self.session.refresh(data_obj)
        return data_obj

    async def get_all(self) -> Sequence[ModelType]:
        """Retrieve all records of a specific model from the database.

        Returns:
            A sequence containing all objects of a specific model.
        """
        db_objs = await self.session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_by_id(self, obj_id: uuid.UUID) -> ModelType | None:
        """Get record of a specific model from the database by ID.

        Args:
            obj_id: Object ID.

        Returns:
            A object of a specific model or None.
        """
        instance = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return instance.scalar_one_or_none()

    async def update(
        self,
        db_obj: ModelType,
        data: BaseModel,
    ) -> ModelType:
        """Update record of a specific model.

        Args:
            db_obj: Database object to update.
            data: The data to update an object.

        Returns:
            Updated object of a specific model.
        """
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: ModelType) -> ModelType:
        """Remove record of a specific model.

        Args:
            db_obj: Database object to remove.

        Returns:
            Removed object of a specific model.
        """
        await self.session.delete(db_obj)
        await self.session.flush()
        return db_obj


class BatteryRepository(BaseRepository[Battery]):
    """Repository for managing battery data interactions with the database."""

    model = Battery


class DeviceRepository(BaseRepository[Device]):
    """Repository for managing device data interactions with the database."""

    model = Device

    async def get_by_name(self, device_name: str) -> Device | None:
        """Get record of a specific model from the database by name.

        Args:
            device_name: Device name.

        Returns:
            A object of a specific model or None.
        """
        instance = await self.session.execute(
            select(self.model).where(self.model.name == device_name)
        )
        return instance.scalar_one_or_none()
