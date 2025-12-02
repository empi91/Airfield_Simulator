from __future__ import annotations

from io import RawIOBase
from time import sleep

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database import Database
from app.exceptions import PlaneOutOfFuelError
from app.logger import Logger
from app.models import Plane as ORMPlane
from app.schemas import Plane
from app.services.plane_controller import PlaneController
from app.services.traffic_controller import TrafficController


class PlaneManager:
    def __init__(self, database: Database, traffic_controller: TrafficController):
        self.db = database
        self.tc = traffic_controller
        self.logger = Logger()
        self.plane_mngr_logger = self.logger.get_logger(
            "plane_manager", ["console", "file"], "DEBUG"
        )

    def __repr__(self) -> str:
        return ""

    def start_operations(self):
        # self.plane_mngr_logger = logger.get_logger(
        #     "plane_manager", ["console", "file"], "DEBUG"
        # )
        planes: list[Plane] = []

        """Creating 5 new planes and adding them to database as ORM models"""
        for _ in range(5):
            try:
                plane = Plane()
                planes.append(plane)
                self.plane_mngr_logger.debug("New plane added to list")
            except ValidationError as e:
                self.plane_mngr_logger.error(f"Validation Error: {e}")
                raise
        try:
            for plane in planes:
                self.db.add_plane(plane)
        except SQLAlchemyError as e:
            self.plane_mngr_logger.error(f"SQLAlchemy Error: {e}")
            raise

        """Getting all planes from database, converting to pydantic (automatically), move them and save back to database"""
        while True:
            try:
                orm_planes: list[ORMPlane] = self.db.get_all_planes()
                self.plane_mngr_logger.debug("Getting all planes from DB")

                for plane in orm_planes:
                    print(plane)
                print(30 * "-")

                plane_controllers = [
                    PlaneController(plane, self.tc) for plane in orm_planes
                ]
                for plane_controller in plane_controllers:
                    try:
                        plane_controller.move_plane(plane_controller.plane)
                    except PlaneOutOfFuelError as e:
                        print(f"Plane {e.plane_id} crashed due to no fuel")

                self.db.update_planes(orm_planes)
                sleep(10)
            except ValidationError as e:
                self.plane_mngr_logger.error(f"Validation Error: {e}")
                raise
                
                print(f"Pydantic Validation Error: {e}")
            except SQLAlchemyError as e:
                self.plane_mngr_logger.error(f"SQLAlchemy Error: {e}")
                RawIOBase

    def connect_planes(self):
        # TODO
        # ADDFEATURE
        pass

    def get_thread(self):
        # TODO
        pass
