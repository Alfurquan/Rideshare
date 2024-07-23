from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import List
from .vehicle import Vehicle
from .user import User

class RideStatus(Enum):
    Started = 'Started'
    Ended = 'Ended'

@dataclass
class Ride:
    source : str
    destination: str
    seats: int
    driver : User = None
    vehicle: Vehicle = None
    fare: int = 0
    ride_status : RideStatus = RideStatus.Started.value
    passengers: List[User] = field(default_factory=list)
    id: int = field(default=None, compare=False)
    
    @classmethod
    def from_dict(cls, d):
        ride = Ride(**d)
        ride.driver = User.from_dict(ride.driver)
        ride.vehicle = Vehicle.from_dict(ride.vehicle)
        passengers = ride.passengers
        ride.passengers = []
        
        for passenger in passengers:
            ride.passengers.append(User.from_dict(passenger))

        return ride
        
    def to_dict(self):
        return asdict(self)
    
    def __hash__(self):
        return self.id
    
@dataclass
class RideDetail:
    rides: List[Ride] = field(default_factory=list)
    total_fare: int = 0
    available_seats: int = 0
    
    # @classmethod
    # def from_dict(cls, d):
    #     ride_detail = RideDetail(**d)
    #     ride_detail.ride = Ride.from_dict(ride_detail.ride)
    #     return ride_detail
        
    # def to_dict(self):
    #     return asdict(self)
    
    def __hash__(self):
        return self.ride
