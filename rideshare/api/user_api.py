from ..data.db import DB
from ..models.user import User
from ..exception import UserNameMissingException, UserPhoneMissingException

class UserAPI:
    def __init__(self, db:DB):
        self.db = db
        self.db.set_table_name('users')
    
    def register_user(self, user: User):
        if not user.name or user.name == ' ':
            raise UserNameMissingException
        
        if not user.phone or user.phone == ' ':
            raise UserPhoneMissingException
        
        id = self.db.create(user.to_dict())
        self.db.update(id, {'id': id})
        return id
    
    def get_user(self, id: int):
        user = self.db.get_item_by_id(id)
        return User.from_dict(user)
    
    def list_users(self):
        users = self.db.get_all()
        
        return [User.from_dict(user) for user in users]
        