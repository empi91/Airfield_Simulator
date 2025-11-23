from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import config
from app.schemas import Plane


class Database():

    def __init__(self):
        """Declaration of database object, used for all database operations"""
        #TODO Check if database exists, if YES continue, if NO create new database

    
    def add_plane(self, plane: Plane):
        """Adding new plane to database"""
        # ADDFEATURE Adding new plane to database

    
    def get_plane(self):
        """Getting plane data from database"""
        # ADDFEATURE Getting plane from DB every second (?) to update it's position


    def update_plade(self):
        """Updating plane data in database"""
        # ADDFEATURE Updating plane's data in database after each time period

    


Base = declarative_base()

engine = create_engine(config.database.database_engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
with Session() as session:
    pass
    

