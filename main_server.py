from app.utils.config import config
from app.connection import Server
from app.database import Database
from app.utils.logger import Logger
from app.services import PlaneManager, TrafficController


def main_server():
    server = Server(config.network.host, config.network.port)
    server.start_server()


def main_plane_manager():
    logger = Logger()
    main_logger = logger.get_logger("main_logger", ["file"], "DEBUG")
    main_logger.debug("Starting program")
    db = Database()
    tc = TrafficController()
    plane_manager = PlaneManager(db, tc)
    db.clear_database()
    plane_manager.start_operations()


if __name__ == "__main__":
    # main_plane_manager()
    main_server()
