import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, override

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.crud import BatteryRepository
from device_monitor.database.base import Base
from device_monitor.database.models import Battery
from device_monitor.schemas import BatteryCreate, BatteryUpdate
from device_monitor.validators import check_battery_exists

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService[ModelType, CreateSchemaType, UpdateSchemaType](ABC):
    """Abstract base class for service handling common functionality."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes this class with a database session.

        Args:
            session: The asynchronous session for database interactions.
        """
        self.session = session

    @abstractmethod
    async def get_all(self) -> Sequence[ModelType]:
        """Retrieve all records of the specified type.

        This method must be implemented by subclasses.

        Returns:
            A sequence containing all records of the specified model type.
        """

    @abstractmethod
    async def create(self, data: CreateSchemaType) -> ModelType:
        """Create record of the specified type.

        This method must be implemented by subclasses.

        Args:
            data: The data to create a new record.

        Returns:
            An instance of the specified model type.
        """

    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID) -> ModelType | None:
        """Retrieve record of the specified type by id.

        This method must be implemented by subclasses.

        Args:
            id_: Record ID.

        Returns:
            An instance of the specified model type.
        """

    @abstractmethod
    async def update(
        self,
        id_: uuid.UUID,
        data: UpdateSchemaType,
    ) -> ModelType | None:
        """Update record of the specified type by id.

        This method must be implemented by subclasses.

        Args:
            id_: Record ID.
            data: The data to update a record.

        Returns:
            An instance of the specified model type.
        """


class BatteryService(BaseService[Battery, BatteryCreate, BatteryUpdate]):
    """Service for managing battery-related operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes this class with a database session.

        Args:
            session: The asynchronous session for database interactions.
        """
        super().__init__(session)
        self.battery_repo = BatteryRepository(session)

    @override
    async def get_all(self) -> Sequence[Battery]:
        """Retrieve all battery records.

        Returns:
            A sequence containing all battery records from the repository.
        """
        return await self.battery_repo.get_all()

    @override
    async def create(self, data: BatteryCreate) -> Battery:
        """Create a battery record.

        Args:
            data: The data to create a new battery record.

        Returns:
            A battery instance from the repository.
        """
        return await self.battery_repo.create(data)

    @override
    async def get_by_id(self, id_: uuid.UUID) -> Battery | None:
        """Retrieve record of the specified type by id.

        Args:
            id_: Record ID.

        Returns:
            The battery record if found; otherwise, None.
        """
        return await check_battery_exists(id_, self.battery_repo)

    @override
    async def update(
        self,
        id_: uuid.UUID,
        data: BatteryUpdate,
    ) -> Battery | None:
        """Update record of the specified type by id.

        Args:
            id_: Record ID.
            data: The data to update a record.

        Returns:
            Updated instance of the battery.
        """
        await check_battery_exists(id_, self.battery_repo)
        return await self.battery_repo.update(id_, data)
