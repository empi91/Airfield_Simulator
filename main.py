# from time import sleep

from app.config import config
from app.connection import Server
from app.operations import PlaneManager


def main_server():
    server = Server(server_host=config.network.host, server_port=config.network.port)
    server.start_server()


def main_plane_manager():
    plane_manager = PlaneManager()
    plane_manager.prepare_env()
    plane_manager.start_operations()


if __name__ == "__main__":
    main_plane_manager()
