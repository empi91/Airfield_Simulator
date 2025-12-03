from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from app.utils.config import config
from app.models import Base
from app.models import Plane as ORMPlane
from app.schemas import Plane as PydanticPlane


class Database:
    def __init__(self):
        """Declaration of database object, used for all database operations"""
        # self.engine = create_engine(config.database.database_engine, echo=True) #TODO Move to echo=True when logging is ready, due to massive size of logs generated
        self.engine = create_engine(config.database.database_engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def __repr__(self) -> str:
        # TODO
        return ""

    def clear_database(self):
        """Clearing all data from database by dropping and recreating tables"""
        try:
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            #TODO Add logging
            print(f"SQLAlchemy error when clearing existing database: {e}")
            raise

    def add_plane(self, plane: PydanticPlane):
        """
        Adding new plane to database
        Converting pydantic plane model to ORM plane model
        Commiting created plane to database
        """
        orm_plane: ORMPlane = self.orm_pydantic_converter(plane)

        try:
            with self.Session() as session:
                session.add(orm_plane)
                session.commit()
        except IntegrityError:
            #TODO Add logging
            raise
        except OperationalError:
            #TODO Add logging
            raise

    def get_all_planes(self) -> list[ORMPlane]:
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
        try:
            with self.Session() as session:
                for plane in planes:
                    orm_plane = (
                        session.query(ORMPlane)
                        .filter(ORMPlane.plane_id == plane.plane_id)
                        .first()
                    )
                    if orm_plane:
                        orm_plane.x_pos = plane.x_pos
                        orm_plane.y_pos = plane.y_pos
                        orm_plane.z_pos = plane.z_pos
                        orm_plane.fuel_left = plane.fuel_left
                        orm_plane.is_landed = plane.is_landed
                session.commit()
        except SQLAlchemyError as e:
            print(f"SQLAlchemy error when updating plane: {e}")
            raise 


    def orm_pydantic_converter(self, plane: PydanticPlane):
        orm_plane: ORMPlane = ORMPlane(
            plane_id=plane.plane_id,
            x_pos=plane.x_pos,
            y_pos=plane.y_pos,
            z_pos=plane.z_pos,
            fuel_left=plane.fuel_left,
            is_landed=plane.is_landed,
        )

        return orm_plane
