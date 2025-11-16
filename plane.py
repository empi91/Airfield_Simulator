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
    # connection: Connection = Connection()

    # def __init__(self, host, port):
    #     """New plane constructor
    #     Generated random UUID4, starting position in 3D world (within limit of the available space)
    #     Assigns default value of starting fuel
    #     """
    #     self.x_pos = randint(0, 100)
    #     self.y_pos = randint(0, 100)
    #     self.z_pos = randint(0, 100)
    #     self.fuel_left = 1000
    #     self.connection = Connection()
    #     self.client_host = host
    #     self.client_port = port

    def __repr__(self):
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane_id} \nCurrent position: \nX: {self.x_pos}\nY: {self.y_pos} \nZ: {self.z_pos} \n Fuel left: {self.fuel_left} \nLanded: {self.is_landed}"

    def start_plane(self):
        connection = Connection()
        with connection.create_connection() as s:
            s.connect((self.client_host, self.client_port))
            print(f"Plane connected: {self}")  # ADDFEATURE Add to logging

    def move_plane(self):
        pass


if __name__ == "__main__":
    plane = Plane(client_host="127.0.0.1", client_port=65432)
    plane.start_plane()
