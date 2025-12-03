"""Test suite for all database operations"""

import unittest

from app.database import Database
from app.schemas import Plane as PydanticPlane
from app.models import Plane as ORMPlane
from app.utils.config import config


class TestDatabase(unittest.TestCase):
    def setUp(self):
        Database.DB_ENGINE = config.tests.DB_ENGINE
        self.db = Database()
        self.db.clear_database()

        """Before each test case"""

    def tearDown(self) -> None:
        """After each test case"""
        self.db.clear_database()
        self.db.close()
        Database.DB_ENGINE = config.database.database_engine

    """Test cases:"""

    def test_adding_plane(self):
        """Test adding single plane to database"""
        # Adding single plane
        plane = PydanticPlane(x_pos=100, y_pos=200, z_pos=3000, fuel_left=1000)
        self.db.add_plane(plane)

        planes = self.db.get_all_planes()
        self.assertEqual(len(planes), 1)
        self.assertEqual(planes[0].x_pos, 100)

    def test_adding_multiple_planes(self):
        """Test adding multpiple planes to DB"""
        # Adding multiple planes
        for _ in range(10):
            plane = PydanticPlane()
            self.db.add_plane(plane)

        planes = self.db.get_all_planes()
        self.assertEqual(len(planes), 10)

    def test_getting_planes_from_empty_db(self):
        """Test getting planes from empty DB"""
        planes = self.db.get_all_planes()
        self.assertEqual(len(planes), 0)

    def test_plane_id(self):
        """Test autoincrementing plane_id in database"""
        for _ in range(10):
            plane = PydanticPlane()
            self.db.add_plane(plane)

        planes = self.db.get_all_planes()
        id = 1

        for plane in planes:
            self.assertIsNotNone(plane.plane_id)
            self.assertEqual(plane.plane_id, id)
            id += 1

    def test_updating_plane_position_fuel(self):
        """Test updating planes position"""
        plane = PydanticPlane(x_pos=100, y_pos=200, z_pos=300, fuel_left=500)
        self.db.add_plane(plane)

        planes = self.db.get_all_planes()
        planes[0].x_pos = 500
        planes[0].fuel_left = 20
        self.db.update_planes(planes)

        updated_planes = self.db.get_all_planes()
        self.assertEqual(updated_planes[0].x_pos, 500)
        self.assertEqual(updated_planes[0].fuel_left, 20)

    def test_clear_database(self):
            """Test database clearing functionality"""
            for _ in range(3):
                self.db.add_plane(PydanticPlane())
            planes = self.db.get_all_planes()
            self.assertEqual(len(planes), 3)
            
            self.db.clear_database()
            planes = self.db.get_all_planes()
            self.assertEqual(len(planes), 0)

    def test_pydantic_sqlalchemy_converter(self):
        pydantic_plane = PydanticPlane(
            x_pos=100, y_pos=200, z_pos=300, 
            fuel_left=800, is_landed=False
        )
        
        orm_plane = self.db.orm_pydantic_converter(pydantic_plane)
        
        self.assertIsInstance(orm_plane, ORMPlane)
        self.assertEqual(orm_plane.x_pos, 100)
        self.assertEqual(orm_plane.fuel_left, 800)
        self.assertEqual(orm_plane.is_landed, False)

    def test_update_nonexistent_plane(self):
            """Test updating a plane that doesn't exist in DB"""
            non_existing_plane = PydanticPlane(plane_id=9999, x_pos=100)
            orm_non_existing = self.db.orm_pydantic_converter(non_existing_plane)
            
            self.db.update_planes([orm_non_existing])
