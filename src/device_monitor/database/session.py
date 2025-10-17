from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from device_monitor.config import get_settings


class DBSession:
    """Database session."""

    def __init__(
        self,
        db_url: str,
        *,
        echo: bool = False,
    ) -> None:
        """Initializes an instance of this class.

        Args:
            db_url: The URL for connecting to the database.
            echo: Outputs the generated sql queries to the console if the value
                is `True`, otherwise not.
        """
        self.db_url = db_url
        self.echo = echo

    def create_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """Creates a session factory for interacting with the database.

        Returns:
            Asyncronous session factory.
        """
        return async_sessionmaker(
            create_async_engine(self.db_url, echo=self.echo),
            expire_on_commit=False,
        )

    async def gen_session(self) -> AsyncGenerator[AsyncSession]:
        """Creates an asynchronous session for interacting with the database.

        Yields:
            Asyncronous session object.
        """
        session_maker = self.create_session_maker()
        async with session_maker() as session:
            yield session


db_session = DBSession(get_settings().db.db_url)
