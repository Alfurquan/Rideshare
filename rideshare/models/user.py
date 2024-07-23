from dataclasses import dataclass, asdict, field

@dataclass
class User:
    name : str = None
    phone: str = None
    id: int = field(default=None, compare=False)
    
    @classmethod
    def from_dict(cls, d):
        return None if d is None else User(**d)
    
    def to_dict(self):
        return asdict(self)
