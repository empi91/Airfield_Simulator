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
    Average fuel consumption: #TODO
    Average plane speed: #TODO
    """
    plane_id: UUID = Field(default_factory=uuid4, frozen=True)
    x_pos: int = randint(0, 10000)
    y_pos: int = randint(0, 10000)
    z_pos: int = randint(2000, 5000)
    fuel_left: int = 1000
    is_landed: bool = False
    # client_host: str
    # client_port: int

class PlaneController():
    """Operation logic behind Plane class object behaviour"""

    def __init__(self):
        """Generating new plane"""
        self.database = Database()


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
