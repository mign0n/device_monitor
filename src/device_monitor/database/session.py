from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from device_monitor.config import get_settings

engine = create_async_engine(get_settings().db.db_url)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
