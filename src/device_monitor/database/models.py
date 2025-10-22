import uuid

from pydantic import NonNegativeFloat
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from device_monitor.database.base import Base


class Battery(Base):
    """Batteries model.

    Attributes:
        __tablename__: Table name in database.
        name: Battery name.
        voltage: Battery nominal voltage.
        residual_capacity: Residual capacity.
        lifespan: Battery lifespan.
        device_id: Foreign key referencing the associated device.
        device: Optional relationship to the associated Device.
    """

    __tablename__ = "batteries"

    name: Mapped[str] = mapped_column()
    voltage: Mapped[NonNegativeFloat] = mapped_column()
    residual_capacity: Mapped[NonNegativeFloat] = mapped_column()
    lifespan: Mapped[NonNegativeFloat] = mapped_column()

    device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("devices.id"),
        nullable=True,
    )

    device: Mapped["Device | None"] = relationship(
        "Device",
        back_populates="batteries",
    )


class Device(Base):
    """Devices model.

    Attributes:
        __tablename__: Table name in database.
        name: Device name.
        firmware_version: Device firmware version.
        status: Device status (on/off).
        batteries: List of associated batteries.
    """

    __tablename__ = "devices"

    name: Mapped[str] = mapped_column(unique=True)
    firmware_version: Mapped[str] = mapped_column()
    status: Mapped[bool] = mapped_column(default=False)

    batteries: Mapped[list["Battery"]] = relationship(
        "Battery",
        back_populates="device",
        cascade="save-update",
        passive_deletes=True,
        lazy="selectin",
    )
