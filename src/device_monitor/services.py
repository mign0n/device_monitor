from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, override

from sqlalchemy.ext.asyncio import AsyncSession

from device_monitor.crud import BatteryRepository
from device_monitor.database.base import Base
from device_monitor.database.models import Battery

ModelType = TypeVar("ModelType", bound=Base)


class BaseService[ModelType](ABC):
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


class BatteryService(BaseService[Battery]):
    """Service for managing battery-related operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes this class with a database session.

        Args:
            session: The asynchronous session for database interactions.
        """
        super().__init__(session)
        self.batery_repo = BatteryRepository(session)

    @override
    async def get_all(self) -> Sequence[Battery]:
        """Retrieve all battery records.

        Returns:
            A sequence containing all battery records from the repository.
        """
        return await self.batery_repo.get_all()
