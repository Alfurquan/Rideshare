from dataclasses import dataclass, asdict, field

@dataclass
class Vehicle:
    model : str = None
    number: str = None
    owner_id: int = None
    id: int = field(default=None, compare=False)
    
    @classmethod
    def from_dict(cls, d):
        return None if d is None else Vehicle(**d)
    
    def to_dict(self):
        return asdict(self)
