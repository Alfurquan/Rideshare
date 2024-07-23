from ..data.db import DB
from ..models.vehicle import Vehicle
from ..models.user import User
from ..api.user_api import UserAPI
from ..exception import VehicleModelMissingException, VehicleNumberMissingException, UserNotFoundException

class VehicleAPI:
    def __init__(self, db: DB, user_api : UserAPI):
        self.db = db
        self.user_api = user_api
        self.db.set_table_name('vehicles')
        
    def register(self, vehicle: Vehicle):
        if vehicle.model is None or vehicle.model == ' ':
            raise VehicleModelMissingException
        
        if vehicle.number is None or vehicle.number == ' ':
            raise VehicleNumberMissingException
        
        user = self.user_api.get_user(vehicle.owner_id)
        
        if user is None:
            raise UserNotFoundException
        
        id = self.db.create(vehicle.to_dict())
        self.db.update(id, {'id': id})
        return id
    
    def get_vehicle(self, id: int):
        return Vehicle.from_dict(self.db.get_item_by_id(id))