import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeFloat


class DeviceCreate(BaseModel):
    """Represents a device data for creating record in the database.

    Attributes:
        name: Device name.
        firmware_version: Device firmware version.
        status: Device status (on/off).
        model_config: Configuration for the Pydantic model, set to accept
            attribute assignment and use enum values.
    """

    name: str
    firmware_version: str
    status: bool = False

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class DeviceDBLight(DeviceCreate):
    """Lightweight device schema for nested serialization.

    Attributes:
        id: Device ID.
    """

    id: uuid.UUID


class DeviceDB(DeviceDBLight):
    """Represents a device in the database.

    Attributes:
        batteries: List of batteries associated with device.
    """

    batteries: list["BatteryDBLight"]


class DeviceUpdate(BaseModel):
    """Represents a device data for updateing record in the database.

    Attributes:
        name: Device name.
        firmware_version: Device firmware version.
        status: Device status (on/off).
        model_config: Configuration for the Pydantic model, set to accept
            attribute assignment and use enum values.
    """

    name: str
    firmware_version: str
    status: bool = False

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class BatteryCreate(BaseModel):
    """Represents a battery data for creating record in the database.

    Attributes:
        name: The name of the battery.
        voltage: The nominal voltage of the battery in volts.
        residual_capacity: The current residual capacity of the battery
            in amp-hours.
        lifespan: The expected lifespan of the battery in hours.
        model_config: Configuration for the Pydantic model, set to accept
            attribute assignment and use enum values.
    """

    name: str
    voltage: NonNegativeFloat
    residual_capacity: NonNegativeFloat
    lifespan: NonNegativeFloat

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class BatteryDBLight(BatteryCreate):
    """Lightweight battery schema for nested serialization.

    Attributes:
        id: Battery ID.
    """

    id: uuid.UUID


class BatteryDB(BatteryDBLight):
    """Represents a battery in the database.

    Attributes:
        device: Device associated with battery.
    """

    device: DeviceDBLight | None = None


class BatteryUpdate(BaseModel):
    """Represents a battery data for updating record in the database.

    Attributes:
        name: The name of the battery.
        voltage: The nominal voltage of the battery in volts.
        residual_capacity: The current residual capacity of the battery
            in amp-hours.
        lifespan: The expected lifespan of the battery in hours.
        device_id: ID of device associated with battery.
        model_config: Configuration for the Pydantic model, set to accept
            attribute assignment and use enum values.
    """

    name: str | None = None
    voltage: NonNegativeFloat | None = None
    residual_capacity: NonNegativeFloat | None = None
    lifespan: NonNegativeFloat | None = None
    device_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
