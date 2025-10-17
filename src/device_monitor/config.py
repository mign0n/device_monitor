import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True, repr=False)
class DBSettings:
    """Database settings.

    Attributes:
        pg_user: User.
        pg_pass: Password.
        pg_host: Host.
        pg_port: Port.
        pg_db: Database name.
    """

    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: int
    pg_db: str

    @property
    def db_url(self) -> str:
        """Generates a URL to connect to the database.

        Returns:
            URL of the database.
        """
        return (
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_pass}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        )


@dataclass(frozen=True)
class Settings:
    """Application settings.

    Attributes:
        db: Database settings.
    """

    db: DBSettings


@lru_cache
def get_settings() -> Settings:
    """Generates application settings.

    Returns:
       The object with the application settings.
    """
    return Settings(
        db=DBSettings(
            pg_user=os.getenv("DB_USER", "postgres"),
            pg_pass=os.getenv("DB_PASS", "postgres"),
            pg_host=os.getenv("DB_HOST", "localhost"),
            pg_port=int(os.getenv("DB_PORT", "5432")),
            pg_db=os.getenv("DB_NAME", "postgres"),
        ),
    )
