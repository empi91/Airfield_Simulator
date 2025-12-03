"""Testing plane management process operated by PlaneManager, PlaneController and TrafficController"""

import logging
import unittest

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.database import Database
from app.schemas import Plane as PydanticPlane
from app.services import PlaneController
from app.services import TrafficController as tc
from app.utils.config import config
from app.utils.exceptions import PlaneOutOfFuelError


class TestPlaneManager(unittest.TestCase):
    def setUp(self):
        Database.DB_ENGINE = config.tests.DB_ENGINE
        self.db = Database()
        self.db.clear_database()
        self.tc = tc()

        """Before each test case"""

    def tearDown(self) -> None:
        """After each test case"""
        self.db.clear_database()
        self.db.close()
        Database.DB_ENGINE = config.database.database_engine

    """Test Cases:"""

    def test_plane_creation_with_defaults(self):
        """Test that Plane creates with valid random defaults"""
        plane = PydanticPlane()
        self.assertIsNotNone(plane.x_pos)
        self.assertIsNotNone(plane.y_pos)
        self.assertIsNotNone(plane.z_pos)
        self.assertEqual(plane.fuel_left, 1000)
        self.assertFalse(plane.is_landed)
        # Checking z_pos boundaries
        self.assertGreaterEqual(plane.z_pos, 2000)
        self.assertLessEqual(plane.z_pos, 5000)

    def test_validation_invalid_fuel(self):
        """Test fuel validation - should be positive integer"""
        with self.assertRaises(ValidationError):
            PydanticPlane(fuel_left="invalid")  # ty: ignore

    def test_validation_invalid_boolean(self):
        """Test is_landed field validation"""
        with self.assertRaises(ValidationError):
            PydanticPlane(is_landed="one")  # ty: ignore

    def test_check_sqlalchemy_errors(self):
        """Test if SQLAchemyErrors are being thrown properly"""
        # ADDFEATURE Add more SQLAlchemy error tests
        plane = PydanticPlane(plane_id=1, x_pos=100, y_pos=200, z_pos=3000)
        self.db.add_plane(plane)

        # Try to add another plane with same ID
        duplicate_plane = PydanticPlane(plane_id=1, x_pos=500, y_pos=600, z_pos=4000)

        with self.assertRaises(IntegrityError):
            self.db.add_plane(duplicate_plane)

    def test_check_no_fuel_left_error(self):
        """Test if PlaneOutOfFuelError is properly handled"""
        plane = PydanticPlane(z_pos=2000, fuel_left=0)
        pc = PlaneController(plane, self.tc)

        with self.assertRaises(PlaneOutOfFuelError) as context:
            pc.move_plane(plane)


class TestPlaneController(unittest.TestCase):
    def setUp(self) -> None:
        self.tc = tc()
        self.plane = PydanticPlane(x_pos=5000, y_pos=5000, z_pos=3000, fuel_left=500)
        self.pc = PlaneController(self.plane, self.tc)
        self.tc.traffic_controller_logger.setLevel(logging.INFO)

    """Test Cases:"""

    def test_fuel_usage(self):
        """Test if plane is using proper amount of fuel in time"""
        initial_fuel = self.plane.fuel_left
        self.pc.move_plane(self.plane)

        expected_fuel = initial_fuel - config.planes.FUEL_CONSUMPTION_DEFAULT
        self.assertEqual(self.plane.fuel_left, expected_fuel)

    def test_fuel_ends(self):
        """Test behavior if plane's fuel reaches 0 during flight"""
        self.plane.fuel_left = config.planes.FUEL_CONSUMPTION_DEFAULT
        self.plane.z_pos = 3000  # In the air

        with self.assertRaises(PlaneOutOfFuelError):
            self.pc.move_plane(self.plane)

    def test_negative_fuel_crash(self):
        """Test that negative fuel causes crash when in air"""
        self.plane.fuel_left = 5  # Less than consumption
        self.plane.z_pos = 2000

        with self.assertRaises(PlaneOutOfFuelError):
            self.pc.move_plane(self.plane)

    def test_plane_moves(self):
        """Test that plane position changes after move"""
        original_x = self.plane.x_pos
        original_y = self.plane.y_pos
        original_z = self.plane.z_pos

        self.pc.move_plane(self.plane)

        # Position should change (ignoring 0, 0, 0 case)
        self.assertNotEqual(original_x, self.plane.x_pos)
        self.assertNotEqual(original_y, self.plane.y_pos)
        self.assertNotEqual(original_z, self.plane.z_pos)


class TestTrafficController(unittest.TestCase):
    def setUp(self) -> None:
        self.tc = tc()
        self.tc.traffic_controller_logger.setLevel(logging.INFO)

    """Test Cases:"""

    def test_plane_movement(self):
        """Test plane movement model, if exceeding boundaries is handled correctly"""

        plane1 = PydanticPlane(
            x_pos=config.aerospace.X_BOUNDARY,
            y_pos=config.aerospace.Y_BOUNDARY,
            z_pos=config.aerospace.MAX_ALTITUDE,
        )
        plane2 = PydanticPlane(x_pos=0, y_pos=0, z_pos=0)

        # Move multiple times to increase chance of hitting boundary
        for _ in range(100):
            self.tc.check_plane_movement(plane1)
            self.tc.check_plane_movement(plane2)

            self.assertLessEqual(plane1.x_pos, config.aerospace.X_BOUNDARY)
            self.assertLessEqual(plane1.y_pos, config.aerospace.Y_BOUNDARY)
            self.assertLessEqual(plane1.z_pos, config.aerospace.MAX_ALTITUDE)

            self.assertGreaterEqual(plane2.z_pos, 0)
            self.assertGreaterEqual(plane2.z_pos, 0)
            self.assertGreaterEqual(plane2.z_pos, 0)
