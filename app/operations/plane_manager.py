from time import sleep

from app.database import Database
from app.schemas import Plane, PlaneController


class PlaneManager:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return ""


    def prepare_env(self):
        db = Database()
        db.check_db_exist()

    def start_operations(self):
        planes: list[Plane] = []
        db = Database()

        """Creating 5 new planes and adding them to database as ORM models"""
        for _ in range(5):
            plane = Plane()
            planes.append(plane)

        for plane in planes:
            db.add_plane(plane)

        """Getting all planes from database, converting to pydantic (automatically), move them and save back to database"""
        while True:
            orm_planes = db.get_all_planes()

            for plane in orm_planes:
                print(plane)

            plane_controllers = [PlaneController(plane) for plane in orm_planes]
            for plane_controller in plane_controllers:
                plane_controller.move_plane(plane_controller.plane)

            db.update_planes(orm_planes)

            sleep(10)

    def connect_planes(self):
        # TODO
        # ADDFEATURE
        pass

    def get_thread(self):
        # TODO
        pass
