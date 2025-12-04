from datetime import datetime
from errno import EPIPE

from app.connection.connection import Connection
from app.utils.config import config
from app.utils.logger import Logger


class Server():
    def __init__(self, server_host: str, server_port: int):
        self.server_host = server_host
        self.server_port = server_port
        self.server_start_time: datetime = datetime.now()
        self.logger = Logger()
        self.server_logger = self.logger.get_logger(
            "server_logger", ["console"], "DEBUG"
        )

    def __repr__(self) -> str:
        return f"Server is running for {datetime.now() - self.server_start_time} with the following configuration: \nHOST: {self.server_host} \nPORT: {self.server_port}"

    def start_server(self):
        """Starting server which is going to manage all incoming planes (connections)"""
        connection = Connection()
        with connection.create_connection(is_server=True) as s:
            s.bind((self.server_host, self.server_port))
            s.listen(config.network.max_connections)
            self.server_logger.info(f"Server online: {self}")

            conn, addr = s.accept()
            with conn:
                self.server_logger.info(f"Client connected: {addr}")
                while True:
                    # TODO Do something with each connected client (plane)

                    ## OLD:
                    # rec_mess = conn.recv(1024).decode("utf-8")
                    # if not rec_mess:
                    #     break

                    try:
                        pass

                    except IOError as e:
                        if e.errno == EPIPE:
                            print("[ERROR] Broken pipe error")
                            break
