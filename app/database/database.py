from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.models import Base
from app.schemas import Plane as PydanticPlane


class Database:
    def __init__(self):
        """Declaration of database object, used for all database operations"""
        # ADDFEATURE Check if database exists, if YES continue, if NO create new database

        self.engine = create_engine(config.database.database_engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_plane(self, plane: PydanticPlane):
        """
        Adding new plane to database
        Converting pydantic plane model to ORM plane model
        Commiting created plane to database
        """
        # ADDFEATURE Adding new plane to database

    def get_all_planes(self) -> list[PydanticPlane]:
        """
        Getting all planes data from database
        Converting them back to pydantic models and returning it in a list
        """
        # ADDFEATURE Getting plane from DB every second (?) to update it's position
        return []

    def update_plane(self, plane: PydanticPlane):
        """
        Updating plane data in database
        Getting ORM plane model from database
        Updating all ORM fields with values passed to method inside pydantic plane
        """
        # ADDFEATURE Updating plane's data in database after each time period
