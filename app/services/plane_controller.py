from app.connection import Connection
from app.schemas import Plane
from app.services.traffic_controller import TrafficController
from app.utils.config import config
from app.utils.exceptions import PlaneOutOfFuelError
from app.utils.logger import Logger


class PlaneController:
    """Operation logic behind Plane class object behaviour
    Average fuel consumption: config.planes.FUEL_CONSUMPTION_DEFAULT
    Average plane speed: #TODO
    """

    def __init__(self, plane: Plane, traffic_controller: TrafficController):
        """Generating new plane"""
        self.plane = plane
        self.tc = traffic_controller
        self.logger = Logger()
        self.plane_controller_logger = self.logger.get_logger(
            "plane_controller", ["file"], "DEBUG"
        )
        self.connect_plane()

    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane.plane_id} \nCurrent position: \nX: {self.plane.x_pos};  Y: {self.plane.y_pos};  Z: {self.plane.z_pos} \nFuel left: {self.plane.fuel_left} \nLanded: {self.plane.is_landed}"

    def connect_plane(self):
        """Connecting created plane to the server"""
        connection = Connection()
        with connection.create_connection() as s:
            s.connect((config.network.host, config.network.port))

            self.plane_controller_logger.info(
                f"Plane {self.plane.plane_id} connected to server."
            )

    def move_plane(self, plane: Plane):
        """Moving plane in 3D space, using fuel and avoiding colisions
        For each Plane in planes list check position, fuel, look for best route to the landing area
        """
        plane: Plane = self.tc.check_plane_movement(plane)
        plane.fuel_left -= config.planes.FUEL_CONSUMPTION_DEFAULT
        print(plane)

        if plane.fuel_left <= 0 and plane.z_pos > 0:
            raise PlaneOutOfFuelError(plane.plane_id)

        return 1
