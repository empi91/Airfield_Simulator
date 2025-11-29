from __future__ import annotations
from time import sleep

from app.models import Plane as ORMPlane
from app.schemas import Plane
from app.database import Database
from app.services.plane_controller import PlaneController
from app.services.traffic_controller import TrafficController


class PlaneManager:
    def __init__(self, database: Database, traffic_controller: TrafficController):
        self.db = database
        self.tc = traffic_controller

    def __repr__(self) -> str:
        return ""

    def start_operations(self):
        planes: list[Plane] = []

        """Creating 5 new planes and adding them to database as ORM models"""
        for _ in range(5):
            plane = Plane()
            planes.append(plane)

        for plane in planes:
            self.db.add_plane(plane)

        """Getting all planes from database, converting to pydantic (automatically), move them and save back to database"""
        while True:
            orm_planes: list[ORMPlane] = self.db.get_all_planes()

            for plane in orm_planes:
                print(plane)
            print(30 * "-")

            plane_controllers = [
                PlaneController(plane, self.tc) 
                for plane in orm_planes]
            for plane_controller in plane_controllers:
                plane_controller.move_plane(plane_controller.plane)

            self.db.update_planes(orm_planes)

            sleep(10)

    def connect_planes(self):
        # TODO
        # ADDFEATURE
        pass

    def get_thread(self):
        # TODO
        pass
