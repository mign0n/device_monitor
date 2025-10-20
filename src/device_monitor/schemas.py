import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeFloat


class BatteryDB(BaseModel):
    """Represents a battery in the database.

    Attributes:
        id: A unique identifier for the battery.
        name: The name of the battery.
        voltage: The nominal voltage of the battery in volts.
        residual_capacity: The current residual capacity of the battery
         in amp-hours.
        lifespan: The expected lifespan of the battery in hours.
        model_config: Configuration for the Pydantic model, set to accept
         attribute assignment and use enum values.
    """

    id: uuid.UUID
    name: str
    voltage: NonNegativeFloat
    residual_capacity: NonNegativeFloat
    lifespan: NonNegativeFloat

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
