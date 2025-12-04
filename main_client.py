"""Client class - creates new planes, connects them to server, allows following their status"""

from app.database import Database
from app.utils.logger import Logger
from app.services import PlaneManager, TrafficController

class Client:
    def __init__(self):

        pass

    def __repr__(self) -> str:
        return ""

    def start_client(self):
        logger = Logger()
        main_logger = logger.get_logger("main_client_logger", ["file"], "DEBUG")
        main_logger.debug("Starting program")
        db = Database()
        tc = TrafficController()
        plane_manager = PlaneManager(db, tc)
        db.clear_database()
        plane_manager.start_operations()


if __name__ == "__main__":
    client = Client()
    client.start_client()
    

