from random import randint
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


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
    x_pos: int = Field(default_factory=lambda: randint(0, 10000))
    y_pos: int = Field(default_factory=lambda: randint(0, 10000))
    z_pos: int = Field(default_factory=lambda: randint(2000, 5000))
    fuel_left: int = 1000
    is_landed: bool = False

    model_config = ConfigDict(from_attributes=True)


class PlaneController:
    """Operation logic behind Plane class object behaviour
    Average fuel consumption: #TODO
    Average plane speed: #TODO
    """

    def __init__(self, plane: Plane):
        """Generating new plane"""
        self.plane = plane

    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane.plane_id} \nCurrent position: \nX: {self.plane.x_pos}\nY: {self.plane.y_pos} \nZ: {self.plane.z_pos} \n Fuel left: {self.plane.fuel_left} \nLanded: {self.plane.is_landed}"

    # def start_plane(self):
    #     """
    #     Creating new plane (connection) to server and checking plane parameters.
    #     Adding newly crated plane to database.
    #     """
    #     connection = Connection()
    #     with connection.create_connection() as s:
    #         s.connect((config.network.host, config.network.port))
    #         print(f"Plane connected: {self}")  # ADDFEATURE Add to logging

    def connect_plane(self):
        """Connecting created plane to the server"""
        # TODO


    def move_plane(self, plane: Plane):
        """Moving plane in 3D space, using fuel and avoiding colisions
        For each Plane in planes list check position, fuel, look for best route to the landing area
        """
        #TODO
        plane.x_pos += randint(-10, 10)
        plane.y_pos += randint(-15, 15)
        plane.z_pos += randint(-10, 10)
        plane.fuel_left -= 10

