from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()

# TODO Check if any secondary tables are required


class Plane(Base):
    """SQLAlchemy Plane model"""

    __tablename__ = "plane"

    plane_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    x_pos: Mapped[int] = mapped_column(Integer)
    y_pos: Mapped[int] = mapped_column(Integer)
    z_pos: Mapped[int] = mapped_column(Integer)
    fuel_left: Mapped[int] = mapped_column(Integer)
    is_landed: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.plane_id} \nCurrent position: \nX: {self.x_pos};  Y: {self.y_pos};  Z: {self.z_pos} \nFuel left: {self.fuel_left} \nLanded: {self.is_landed}"


class Collision(Base):
    """SQLAlchemy model of collisions table"""

    __tablename__ = "collision"

    collision_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    plane_1_id: Mapped[Plane] = mapped_column(Integer, ForeignKey("plane.plane_id"))
    plane_2_id: Mapped[Plane] = mapped_column(Integer, ForeignKey("plane.plane_id"))
