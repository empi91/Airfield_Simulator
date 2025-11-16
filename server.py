from datetime import datetime
from connection import Connection
from pydantic import BaseModel
from errno import EPIPE


class Server(BaseModel):
    server_start_time: datetime = datetime.now()
    server_host: str
    server_port: int

    def __repr__(self):
        return f"Server is running for {datetime.now() - self.server_start_time} with the following configuration: \nHOST: {self.server_host} \nPORT: {self.server_port}"

    def start_server(self):
        """Starting server which is going to manage all incoming planes (connections)"""
        connection = Connection()
        with connection.create_connection(is_server=True) as s:
            s.bind((self.server_host, self.server_port))
            s.listen(100)
            print("Server online")  # ADDFEATURE add it to logging
            print(f"Server: {self}")

            conn, addr = s.accept()
            with conn:
                print(f"Client connected: {addr}")  # ADDFEATURE Add to logging
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
