from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Plane(BaseModel):
    plane_id: UUID = Field(default_factory=uuid4, frozen=True)
    x_pos: int
    y_pos: int
    z_pos: int
    fuel_left: int
    is_landed: bool = False


    def __init__(self):
        """New plane constructor
        Generated random UUID4, starting position in 3D world (within limit of the available space)
        Assigns default value of starting fuel
        """
        pass


    def __repr__(self):
        """Method for printing plane info for debugging purposes"""
        return(f"Plane {self.plane_id} \nCurrent position: \nX: {self.x_pos}\nY: {self.y_pos} \nZ: {self.z_pos} \n Fuel left: {self.fuel_left} \nLanded: {self.is_landed}")


    def move_plane(self):

        pass
