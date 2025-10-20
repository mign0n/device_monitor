import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeFloat


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


class BatteryDB(BatteryCreate):
    """Represents a battery in the database.

    Attributes:
        id: A unique identifier for the battery.
    """

    id: uuid.UUID


class BatteryUpdate(BaseModel):
    """Represents a battery data for updating record in the database.

    Attributes:
        name: The name of the battery.
        voltage: The nominal voltage of the battery in volts.
        residual_capacity: The current residual capacity of the battery
            in amp-hours.
        lifespan: The expected lifespan of the battery in hours.
        model_config: Configuration for the Pydantic model, set to accept
            attribute assignment and use enum values.
    """

    name: str | None = None
    voltage: NonNegativeFloat | None = None
    residual_capacity: NonNegativeFloat | None = None
    lifespan: NonNegativeFloat | None = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
