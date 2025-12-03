from random import randint

from app.schemas import Plane
from app.utils.config import config
from app.utils.logger import Logger


class TrafficController:
    def __init__(self):
        self.logger = Logger()
        self.traffic_controller_logger = self.logger.get_logger(
            "traffic_controller_logger", ["file", "console"], "DEBUG"
        )

    def __repr__(self) -> str:
        return ""

    def check_plane_movement(self, plane: Plane) -> Plane:
        plane.x_pos += randint(-10, 10)
        plane.y_pos += randint(-10, 10)
        plane.z_pos += randint(-10, 10)

        plane.x_pos = max(0, min(config.aerospace.X_BOUNDARY, plane.x_pos))
        plane.y_pos = max(0, min(config.aerospace.Y_BOUNDARY, plane.y_pos))
        plane.z_pos = max(0, min(config.aerospace.MAX_ALTITUDE, plane.z_pos))

        self.traffic_controller_logger.debug(f"Plane {plane.plane_id} finished moving")

        return plane
