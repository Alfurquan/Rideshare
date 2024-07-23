from typing import List
from ..models.ride import Ride, RideDetail, RideStatus
from ..data.db import DB
from ..api.user_api import UserAPI
from ..api.vehicle_api import VehicleAPI
from ..strategy.selection_strategy import Strategy, RideSelectionStrategyFactory
from ..exception import UserNotFoundException, RideDoesNotExists, FareNegativeException, UserNotOwningVehicleException, VehicleNotFoundException, SeatsNegativeException, SourceEmptyException, DestinationEmptyException, RideAlreadyOfferedWithSameVehicleException

class RideAPI:
    def __init__(self, db: DB, user_api: UserAPI, vehicle_api: VehicleAPI):
        self.db = db
        self.user_api = user_api
        self.vehicle_api = vehicle_api
        self.db.set_table_name('Rides')
        
    def offer_ride(self, driver: int, source: str, destination: str, seats: int, fare: int, vehicle_id: int):
        if source is None or source == ' ':
            raise SourceEmptyException
        
        if destination is None or destination == ' ':
            raise DestinationEmptyException
        
        if seats < 0:
            raise SeatsNegativeException
        
        if fare < 0:
            raise FareNegativeException
        
        user = self.user_api.get_user(driver)
        if user is None:
            raise UserNotFoundException
        
        vehicle = self.vehicle_api.get_vehicle(vehicle_id)
        
        if vehicle is None:
            raise VehicleNotFoundException
        
        if vehicle.owner_id != driver:
            raise UserNotOwningVehicleException
        
        rides = self.get_rides_for_user(driver)
        
        started_rides_with_vehicle = [ride for ride in rides if ride.vehicle.id == vehicle_id and ride.ride_status == RideStatus.Started.value]
        
        if len(started_rides_with_vehicle) > 0:
            raise RideAlreadyOfferedWithSameVehicleException
        
        ride = Ride(source, destination, seats, user, vehicle, fare)
        id = self.db.create(ride.to_dict())
        self.db.update(id, {'id': id})
        return id
    
    def search_ride(self, source: str, destination: str, seats: int, strategy: Strategy):
        if source is None or source == ' ':
            raise SourceEmptyException
        
        if destination is None or destination == ' ':
            raise DestinationEmptyException
        
        if seats < 0:
            raise SeatsNegativeException
    
        rides = self.db.get_all()
        
        rides = [Ride.from_dict(ride) for ride in rides]

        rides = [ride for ride in rides if ride.ride_status == RideStatus.Started.value and ride.seats >= seats]
        rides = self.get_rides_for_route(rides, source, destination)
        ride_selection = RideSelectionStrategyFactory.get_selection_strategy(strategy)
        return ride_selection.select_ride(rides)
    
    def select_rides(self, rides: List[Ride], user_ids: List[str]):
        
        no_of_selected_seats = len(user_ids)
        
        for ride in rides:
            for user_id in user_ids:
                user = self.user_api.get_user(int(user_id))

                if user is None:
                    raise UserNotFoundException
            
                ride.passengers.append(user)
            ride.seats = ride.seats - no_of_selected_seats
            self.db.update(ride.id, ride.to_dict())
        
    
    def end_ride(self, ride_id: int):
        ride = self.get_ride(ride_id)
        
        if ride is None:
            raise RideDoesNotExists
        
        ride.ride_status = RideStatus.Ended.value
        self.db.update(ride_id, ride.to_dict())
        
    def get_ride_stats(self):
        users = self.user_api.list_users()
        
        rides = [Ride.from_dict(ride) for ride in self.db.get_all()]
        
        ride_stats = {}
        
        for user in users:
            if not user.name in ride_stats:
                ride_stats[user.name] = {
                    'rides_taken': 0,
                    'rides_offered': 0
                }
            for ride in rides:
                if ride.driver.id == user.id:
                    ride_stats[user.name]['rides_offered'] = ride_stats[user.name]['rides_offered'] + 1

                for passenger in ride.passengers:
                    if passenger.id == user.id:
                        ride_stats[user.name]['rides_taken'] = ride_stats[user.name]['rides_taken'] + 1
            
        return ride_stats
    
    def get_rides_for_user(self, user_id):
        rides = self.db.get_all()
        results: List[Ride] = [
                    Ride.from_dict(ride) for ride in rides 
                    if Ride.from_dict(ride).driver.id == user_id
                ]
        return results

    
    def get_rides_for_route(self, rides: List[Ride], source: str, destination: str):        
    
        rides_graph = self.construct_ride_graph(rides)
        
        results: List[RideDetail] = []
        
        def dfs(source, destination, tmp_res):        
            if source.lower() == destination.lower():
                ride_detail = RideDetail(rides=list(tmp_res))
                ride_detail.available_seats = min(ride.seats for ride in tmp_res)
                ride_detail.total_fare = sum(ride.fare for ride in tmp_res)
                results.append(ride_detail)
                return

            if not source in rides_graph:
                return

            for ride in rides_graph[source]:
                tmp_res.append(ride)                
                dfs(ride.destination, destination, tmp_res)
                tmp_res.pop()
        
        dfs(source, destination, [])
            
        return results
        
    def get_rides_for_route_dfs(self, rides_graph, source, destination, results, rides):        
        if not source in rides_graph:
            return
        
        if source == destination:
            results.append(rides)
            return
        
        for ride in rides_graph[source]:
            rides.append(RideDetail(ride))
            self.get_rides_for_route_dfs(rides_graph, ride.destination, destination, results, rides)
            rides.pop()
        
    def construct_ride_graph(self, rides: List[Ride]):
        rides_graph = {}

        for ride in rides:
            rides_graph.setdefault(ride.source, []).append(ride)
                        
        return rides_graph
    
    def get_ride(self, ride_id):
        ride = self.db.get_item_by_id(ride_id)
        return Ride.from_dict(ride)
        
        
            