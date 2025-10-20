from pydantic import NonNegativeFloat
from sqlalchemy.orm import Mapped, mapped_column

from device_monitor.database.base import Base


class Battery(Base):
    """Batteries model.

    Attributes:
        __tablename__: Table name in database.
        name: Battery name.
        voltage: Battery nominal voltage.
        residual_capacity: Residual capacity.
        lifespan: Battery lifespan.
    """

    __tablename__ = "batteries"

    name: Mapped[str] = mapped_column()
    voltage: Mapped[NonNegativeFloat] = mapped_column()
    residual_capacity: Mapped[NonNegativeFloat] = mapped_column()
    lifespan: Mapped[NonNegativeFloat] = mapped_column()
