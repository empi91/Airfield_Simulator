"""Custom exceptions for the project"""

class AirfieldSimulatorError(Exception):
    """Base exception for all custom exceptions"""
    pass

class PlaneOutOfFuelError(AirfieldSimulatorError):
    """Raised when plane has insufficient fuel"""

    def __init__(self, plane_id: int| None):
        self.plane_id = plane_id
        super().__init__(f"Plane {plane_id} crashed due to no fuel left")   

class AirspaceViolationError(AirfieldSimulatorError):
    """Raised when plane exceeds aerospace boundaries"""
    pass

class PlaneCollisionError(AirfieldSimulatorError):
    """Raised when plane collision is detected"""
    pass