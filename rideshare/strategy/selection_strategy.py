from enum import Enum
from abc import ABC, abstractmethod
from typing import List
from ..models.ride import RideDetail

class Strategy(Enum):
    MOST_VACANT = 'Most_vacant'
    MOST_CHEAPEST = 'Most_cheapest'
    
class RideSelection(ABC):
    
    @abstractmethod
    def select_ride(self, rides : List[RideDetail]):
        raise NotImplementedError
    

class CheapestRideSelection(RideSelection):
    
    def select_ride(self, rides: List[RideDetail]):
        return sorted(rides, key = lambda ride: ride.total_fare)
    
    
class MostVacantRideSelection(RideSelection):
    
    def select_ride(self, rides: List[RideDetail]):
        return sorted(rides, key = lambda ride: ride.available_seats, reverse=True)
    

class RideSelectionStrategyFactory:
    
    @classmethod
    def get_selection_strategy(cls, strategy: Strategy):
        return MostVacantRideSelection() if strategy == Strategy.MOST_VACANT else CheapestRideSelection()