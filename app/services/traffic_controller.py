from app.schemas import Plane

from random import randint
from app.config import config


class TrafficController:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return ""

    @staticmethod
    def check_plane_movement(plane: Plane) -> Plane:
        plane.x_pos += randint(-10, 10)
        plane.y_pos += randint(-10, 10)
        plane.z_pos += randint(-10, 10)

        plane.x_pos = max(0, min(config.aerospace.X_BOUNDARY, plane.x_pos))
        plane.y_pos = max(0, min(config.aerospace.Y_BOUNDARY, plane.y_pos))
        plane.z_pos = max(0, min(config.aerospace.MAX_ALTITUDE, plane.z_pos))

        return plane
