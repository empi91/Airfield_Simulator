from server import Server

def main():
    server = Server(server_host="127.0.0.1", server_port=65432)
    server.start_server()



if __name__ == "__main__":
    main()
