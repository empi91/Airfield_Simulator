from random import randint
# from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict
from app.config import config


class Plane(BaseModel):
    """New plane pydantic model
    Each plane has an unique ID
    Each plane arrives in random area, on the height between 2 and 5km
    Each plane arrives with full fuel tank.
    """

    # plane_id: UUID = Field(
    #     default_factory=uuid4, frozen=True
    # )  # BUG Apply uuid properly working with different types of database (probably to be implemented in SQLAlchemy model)
    plane_id: int | None = Field(default=None)
    x_pos: int = Field(default_factory=lambda: randint(0, config.aerospace.X_BOUNDARY))
    y_pos: int = Field(default_factory=lambda: randint(0, config.aerospace.Y_BOUNDARY))
    z_pos: int = Field(default_factory=lambda: randint(2000, config.aerospace.MAX_ALTITUDE))
    fuel_left: int = 1000
    is_landed: bool = False

    model_config = ConfigDict(from_attributes=True)
