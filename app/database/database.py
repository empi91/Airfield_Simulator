from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.models import Base
from app.models import Plane as ORMPlane
from app.schemas import Plane as PydanticPlane


class Database:
    def __init__(self):
        """Declaration of database object, used for all database operations"""
        self.engine = create_engine(config.database.database_engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def __repr__(self) -> str:
        # TODO
        return ""

    def check_db_exist(self):
        """Checking if there is already an existing SQlite database and removing it to avoid using old data"""
        file_path = Path("test_db.db")
        if file_path.exists():
            file_path.unlink(missing_ok=True)

    def add_plane(self, plane: PydanticPlane) -> int:
        """
        Adding new plane to database
        Converting pydantic plane model to ORM plane model
        Commiting created plane to database
        """
        orm_plane: ORMPlane = self.orm_pydantic_converter(plane)
        with self.Session() as session:
            session.add(orm_plane)
            session.commit()

        return 1

    def get_all_planes(self) -> list[PydanticPlane]:
        """
        Getting all planes data from database
        Converting them back to pydantic models and returning it in a list
        """
        planes = []
        with self.Session() as session:
            orm_planes = session.query(ORMPlane).all()

            for plane in orm_planes:
                planes.append(plane)
        return planes

    def update_planes(self, planes: list[ORMPlane]):
        """
        Updating plane data in database
        Getting ORM plane model from database
        Updating all ORM fields with values passed to method inside pydantic plane
        """
        for plane in planes:
            with self.Session() as session:
                orm_plane = (
                    session.query(ORMPlane)
                    .filter(ORMPlane.Plane_id == plane.Plane_id)
                    .first()
                )
                if orm_plane:
                    orm_plane.x_pos = plane.x_pos
                    orm_plane.y_pos = plane.y_pos
                    orm_plane.z_pos = plane.z_pos
                    orm_plane.fuel_left = plane.fuel_left
                    orm_plane.is_landed = plane.is_landed
                    session.commit()

    def orm_pydantic_converter(self, plane: PydanticPlane):
        orm_plane: ORMPlane = ORMPlane(
            Plane_id=plane.plane_id,
            x_pos=plane.x_pos,
            y_pos=plane.y_pos,
            z_pos=plane.z_pos,
            fuel_left=plane.fuel_left,
            is_landed=plane.is_landed,
        )

        return orm_plane
