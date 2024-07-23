class UserNameMissingException(Exception):
    pass

class UserPhoneMissingException(Exception):
    pass

class VehicleModelMissingException(Exception):
    pass

class VehicleNumberMissingException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class VehicleNotFoundException(Exception):
    pass

class SourceEmptyException(Exception):
    pass

class DestinationEmptyException(Exception):
    pass

class SeatsNegativeException(Exception):
    pass

class FareNegativeException(Exception):
    pass

class UserNotOwningVehicleException(Exception):
    pass

class RideAlreadyOfferedWithSameVehicleException(Exception):
    pass

class RideDoesNotExists(Exception):
    pass