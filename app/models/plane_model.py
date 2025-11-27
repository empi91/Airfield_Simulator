from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, declarative_base



Base = declarative_base()

# TODO Check if any secondary tables are required


class Plane(Base):
    """SQLAlchemy Plane model"""
    __tablename__ = "plane"

    Plane_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    x_pos: Mapped[int] = mapped_column(Integer)
    y_pos: Mapped[int] = mapped_column(Integer)
    z_pos: Mapped[int] = mapped_column(Integer)
    fuel_left: Mapped[int] = mapped_column(Integer)
    is_landed: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        """Method for printing plane info for debugging purposes"""
        return f"Plane {self.Plane_id} \nCurrent position: \nX: {self.x_pos}\nY: {self.y_pos} \nZ: {self.z_pos} \n Fuel left: {self.fuel_left} \nLanded: {self.is_landed}"

