import socket
import unittest
from unittest.mock import MagicMock, patch

from app.connection import Connection, Server


class TestConnection(unittest.TestCase):
    def test_create_client_connection_success(self):
        """
        Tests that a client socket is created successfully.
        """
        connection = Connection()
        sock = connection.create_connection(is_server=False)

        self.assertIsNotNone(sock)
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(connection.socket, sock)
        connection.close()

    def test_create_server_connection_success(self):
        """
        Tests that a server socket is created with the correct options (SO_REUSEADDR).
        """
        connection = Connection()
        sock = connection.create_connection(is_server=True)

        self.assertIsNotNone(sock)
        self.assertIsInstance(sock, socket.socket)

        sock.bind(("127.0.0.1", 0))  # Assigning to port choosen by OS
        port = sock.getsockname()[1]
        sock.close()

        connection2 = Connection()
        sock2 = connection2.create_connection(is_server=True)
        sock2.bind(("127.0.0.1", port))

        connection2.close()

    def test_connection_close(self):
        """
        Tests that the close method correctly closes the socket.
        """
        connection = Connection()
        connection.create_connection()

        self.assertIsNotNone(connection.socket)
        connection.close()
        self.assertIsNone(connection.socket)

    def test_connection_creation_failure(self):
        """
        Tests that the connection creation handles socket errors.
        """
        with patch("app.connection.connection.socket.socket") as mock_socket:
            mock_socket.side_effect = socket.error("Connection failed")

            connection = Connection()
            result = connection.create_connection()

            self.assertIsNone(result)
            self.assertIsNone(connection.socket)


class TestServer(unittest.TestCase):
    @patch("app.connection.server.Logger")
    @patch("app.connection.server.Database")
    def test_server_initialization(self, mock_database, mock_logger):
        """
        Tests that the Server class initializes with the correct host and port.
        """
        server = Server("127.0.0.1", 8080)

        self.assertEqual(server.server_host, "127.0.0.1")
        self.assertEqual(server.server_port, 8080)
        self.assertIsNotNone(server.server_start_time)
        self.assertIsNotNone(server.db)
        self.assertIsNotNone(server.logger)

    @patch("app.connection.server.Logger")
    @patch("app.connection.server.Database")
    def test_server_binds_and_listens(self, mock_database, mock_logger):
        """
        Tests that the server correctly binds to a host/port and starts listening.
        """
        server = Server("127.0.0.1", 0)

        with patch.object(socket.socket, "accept", side_effect=KeyboardInterrupt()):
            server.start_server()

    @patch("app.connection.server.Database")
    @patch("app.connection.server.Logger")
    def test_server_accepts_connection(self, mock_logger, mock_database):
        """
        Tests that the server can accept an incoming client connection.
        """
        server = Server("127.0.0.1", 0)

        mock_client_conn = MagicMock()
        mock_addr = ("192.168.1.100", 5000)

        with patch.object(
            socket.socket, "accept", return_value=(mock_client_conn, mock_addr)
        ):
            mock_database.return_value.get_all_planes.side_effect = KeyboardInterrupt()
            server.start_server()


if __name__ == "__main__":
    unittest.main()
