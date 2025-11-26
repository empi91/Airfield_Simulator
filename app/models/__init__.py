"""SQLAlchemy models module for database entities.

Note: The Plane class here is the SQLAlchemy ORM model for database operations.
For the Pydantic schema used in business logic, see app.schemas.Plane.
"""

from app.models.plane_model import Base, Plane

__all__ = ["Base", "Plane"]
