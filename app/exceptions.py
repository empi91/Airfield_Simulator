"""Custom exceptions for the project"""

from app.logger import Logger


class AirfieldSimulatorError(Exception):
    """Base exception for all custom exceptions"""

    def __init__(self, error_msg):
        self.error_msg = error_msg
        self.logger = Logger()
        self.exception_logger = self.logger.get_logger(
            "exception_logger", ["file", "console"], "ERROR"
        )

    def __str__(self):
        self.exception_logger.error(self.error_msg)
        return self.error_msg


class PlaneOutOfFuelError(AirfieldSimulatorError):
    """Raised when plane has insufficient fuel"""

    def __init__(self, plane_id: int | None):
        self.plane_id = plane_id
        super().__init__(f"Plane {plane_id} crashed due to no fuel left")


class AirspaceViolationError(AirfieldSimulatorError):
    """Raised when plane exceeds aerospace boundaries"""

    pass


class PlaneCollisionError(AirfieldSimulatorError):
    """Raised when plane collision is detected"""

    pass
