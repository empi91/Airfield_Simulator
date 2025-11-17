from server import Server
from config import config

def main():
    # server = Server(server_host="127.0.0.1", server_port=65432)
    server = Server(server_host=config.network.host, server_port=config.network.port)
    server.start_server()



if __name__ == "__main__":
    main()
