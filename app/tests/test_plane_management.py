"""Testing plane management process operated by PlaneManager, PlaneController and TrafficController"""

import unittest

class TestPlaneManager(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    """Test Cases:"""
    def test_validation(self):
        """Test if Pydantic ValidationErrors are being thrown properly"""

    def check_sqlalchemy_errors(self):
        """Test if SQLAchemyErrors are being thrown properly"""

    def check_no_fuel_left_error(self):
        """Test if PlaneOutOfFuelError is properly handled"""



class TestPlaneController(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    """Test Cases:"""
    def test_fuel_usage(self):
        """Test if plane is using proper amount of fuel in time"""

    def test_fuel_ends(self):
        """Test behavior if plane's fuel reaches 0 during flight"""


class TestTrafficController(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    """Test Cases:"""
    def test_plane_movement(self):
        """Test plane movement model, if exceeding boundaries is handled correctly"""