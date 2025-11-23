from random import randint
from time import sleep
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.config.config import config
from app.connection import Connection
from app.database import Database


class Plane(BaseModel):
    """New plane pydantic model
    Each plane has an unique ID
    Each plane arrives in random area, on the height between 2 and 5km
    Each plane arrives with full fuel tank. 
    """
    plane_id: UUID = Field(default_factory=uuid4, frozen=True) # BUG Apply uuid properly working with different types of database (probably to be implemented in SQLAlchemy model)
    x_pos: int = Field(default_factory=lambda: randint(0, 10000))
    y_pos: int = Field(default_factory=lambda: randint(0, 10000))
    z_pos: int = Field(default_factory=lambda: randint(2000, 5000))
    fuel_left: int = 1000
    is_landed: bool = False

class PlaneController():
    """Operation logic behind Plane class object behaviour
    Average fuel consumption: #TODO
    Average plane speed: #TODO
    """

    def __init__(self, plane: Plane):
        """Generating new plane"""
        self.database = Database()
        self.plane_id = plane.plane_id
        self.x_pos = plane.x_pos
        self.y_pos = plane.y_pos
        self.z_pos = plane.z_pos
        self.fuel_left = plane.fuel_left
        self.is_landed = plane.is_landed


    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane_id} \nCurrent position: \nX: {self.x_pos}\nY: {self.y_pos} \nZ: {self.z_pos} \n Fuel left: {self.fuel_left} \nLanded: {self.is_landed}"

    def start_plane(self):
        """
        Creating new plane (connection) to server and checking plane parameters.
        Adding newly crated plane to database.
        """
        self.database.add_plane(self)
        connection = Connection()
        with connection.create_connection() as s:
            s.connect((config.network.host, config.network.port))
            print(f"Plane connected: {self}")  # ADDFEATURE Add to logging

    def move_plane(self):
        """Moving plane in 3D space, using fuel and avoiding colisions (#TODO)"""


if __name__ == "__main__":
    # plane = Plane(client_host=config.network.host, client_port=config.network.port)
    plane = Plane()
    plane.start_plane()
    while True:
        plane.move_plane()
        plane.fuel_left -= 1
        print(plane)
        sleep(1)
