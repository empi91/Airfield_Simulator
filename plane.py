from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from connection import Connection
from random import randint


class Plane(BaseModel):
    plane_id: UUID = Field(default_factory=uuid4, frozen=True)
    x_pos: int = randint(0, 100)
    y_pos: int = randint(0, 100)
    z_pos: int = randint(0, 100)
    fuel_left: int = 1000
    is_landed: bool = False
    client_host: str
    client_port: int

    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane_id} \nCurrent position: \nX: {self.x_pos}\nY: {self.y_pos} \nZ: {self.z_pos} \n Fuel left: {self.fuel_left} \nLanded: {self.is_landed}"

    def start_plane(self):
        """
        Creating new plane (connection) to server and checking plane parameters
        """
        connection = Connection()
        with connection.create_connection() as s:
            s.connect((self.client_host, self.client_port))
            print(f"Plane connected: {self}")  # ADDFEATURE Add to logging


if __name__ == "__main__":
    plane = Plane(client_host="127.0.0.1", client_port=65432)
    plane.start_plane()
