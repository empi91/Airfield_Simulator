from app.config import config
from app.connection import Server
from app.services import PlaneManager
from app.database import Database
from app.services import TrafficController
from app.logger import Logger


def main_server():
    server = Server(server_host=config.network.host, server_port=config.network.port)
    server.start_server()


def main_plane_manager():
    logger = Logger()
    main_logger = logger.get_logger("main_logger")
    main_logger.debug("Starting program")
    db = Database()
    tc = TrafficController()
    plane_manager = PlaneManager(db, tc)
    db.clear_database()
    plane_manager.start_operations()


if __name__ == "__main__":
    main_plane_manager()
