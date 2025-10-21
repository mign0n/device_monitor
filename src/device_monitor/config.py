from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings.

    Attributes:
        title: Application title.
        description: Application description.
        docs_url: Swagger url.
        redoc_url: ReDoc url.
        host: Application host.
        port: Application port.
        debug: Is debug mode.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        env_nested_delimiter="_",
        env_nested_max_split=1,
        env_prefix="APP_",
        extra="ignore",
    )
    title: str = "Application title"
    description: str = ""
    docs_url: str | None = None
    redoc_url: str | None = None
    host: str
    port: int
    root_path: str = "/api"
    debug: bool = False


class DBSettings(BaseSettings):
    """Database settings.

    Attributes:
        user: User.
        password: Password.
        host: Host.
        port: Port.
        name: Database name.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        env_nested_delimiter="_",
        env_nested_max_split=1,
        env_prefix="DB_",
        extra="ignore",
    )
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def db_url(self) -> str:
        """Generates a URL to connect to the database.

        Returns:
            URL of the database.
        """
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        app: Application settings.
        db: Database settings.
    """

    app: AppSettings
    db: DBSettings


@lru_cache
def get_settings() -> Settings:
    """Generates application settings.

    Returns:
       The object with the application settings.
    """
    return Settings(app=AppSettings(), db=DBSettings())  # type: ignore[call-arg]
