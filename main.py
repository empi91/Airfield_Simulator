# from time import sleep

from app.config.config import config

# from plane import Plane
from app.connection.server import Server


def main():
    server = Server(server_host=config.network.host, server_port=config.network.port)
    server.start_server()


if __name__ == "__main__":
    main()
