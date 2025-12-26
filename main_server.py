from multiprocessing import Process

from app.connection import Server
from app.database import Database
from app.services import PlaneManager, TrafficController
from app.utils.config import config
from app.utils.logger import Logger
from app.visualisation.airport_space import WebLayout


def main_server():
    server = Server(config.network.host, config.network.port)
    server.start_server()


def main_dashboard():
    """Run the Dash web dashboard"""
    dashboard = WebLayout()
    dashboard.run(debug=False, port=8050)


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
    # Run socket server and dashboard in separate processes
    server_process = Process(target=main_server)
    dashboard_process = Process(target=main_dashboard)

    server_process.start()
    dashboard_process.start()

    try:
        server_process.join()
        dashboard_process.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server_process.terminate()
        dashboard_process.terminate()
        server_process.join()
        dashboard_process.join()
